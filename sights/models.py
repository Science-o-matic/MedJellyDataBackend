# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from lxml import etree as ET


class Sight(models.Model):
    timestamp = models.DateTimeField(verbose_name="Data de medició")
    comments = models.TextField(blank=True)
    beach = models.ForeignKey('Beach', verbose_name="Platja")
    reported_from = models.ForeignKey('ReportingClient')
    variables = models.ManyToManyField("BeachVariable", through="SightVariables")
    validated = models.BooleanField(default=False, verbose_name="Validat")
    sent = models.BooleanField(default=False, verbose_name="Enviat")
    sent_timestamp = models.DateTimeField(verbose_name="Data de enviament", null=True)

    def __unicode__(self):
        return u"%s (%s)" % (unicode(self.beach), self.beach.code)

    def sent_sight(self):
        if self.validated and not self.sent:
            self._sent_sight()

    def _sent_sight():
        root = ET.Element('six')
        code = "ICM%s-%s" % (self.id, self.timestamp.strftime('%Y%m%d'))
        timestamp = self.timestamp.strftime('%d/%m/%Y %H:00')
        sight = ET.Element('mostreig', codi=code, tipus="PLAJ", timestamp=timestamp,
                           observacions="prueba" if settings.DEBUG else "")
        for group in VariablesGroup.objects.all():
            sight.append(ET.Element('grup', codi=group.name, observacions=""))
            for sightvariable in SightVariables.objects.filter(sight=self,
                                                               variable__variable__group=group):
                var = ET.Element('var')
                var_timestamp = ET.Element("timestamp")
                var_timestamp.text = str(timestamp)
                var.append(var_timestamp)
                var_estacio = ET.Element("estacio")
                var_estacio.text = self.beach.code
                var.append(var_estacio)
                var_sightvariable = ET.Element("variable")
                var_sightvariable.text = sightvariable.variable.code
                var.append(var_sightvariable)
                var_profunditat = ET.Element("profunditat")
                var_profunditat.text = "1"
                var.append(var_profunditat)
                var_valor = ET.Element("valor")
                var_valor.text = str(sightvariable.value)
                var.append(var_valor)
                var_motiuInvalid = ET.Element("motiuInvalidacio")
                var_motiuInvalid.text = "0"
                var.append(ET.Element("motiuInvalidacio"))
                var.append(ET.Element("anotacio"))
                var_unitatMesura = ET.Element("unitatMesura")
                var_unitatMesura.text = sightvariable.variable.variable.measure_unit.name
                var.append(var_unitatMesura)
                sight.append(var)
        root.append(sight)

        tree = ET.ElementTree(root)
        tree.write("sight_%s.xml" % code, pretty_print=True,
                   xml_declaration=True, encoding="ISO-8859-1")


    class Meta:
        verbose_name = "Avistamiento"


class Beach(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=1000)
    city = models.ForeignKey("City")
    owner = models.ForeignKey("BeachOwner")
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Playa"


class City(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"


class BeachOwner(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Propietario"


class VariablesGroup(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name

    @property
    def fieldset_name(self):
        fieldset_name = self.name.strip().lower().replace(" ", "_")
        return fieldset_name.encode("ascii", "ignore").replace("'", "")

    class Meta:
        verbose_name = "Grupo de Variables"
        verbose_name_plural = "Grupos de Variables"

class MeasureUnit(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_default(self):
        try:
            return self.objects.get(id=1)
        except:
            return 1

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"


class Variable(models.Model):
    group = models.ForeignKey('VariablesGroup', null=True)
    type = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    measure_unit = models.ForeignKey('MeasureUnit',
                                     default = MeasureUnit.get_default)
    label = models.CharField(max_length=300, null=True)
    FIELD_TYPES = (
        ('BooleanField', 'BooleanField'),
        ('CharField', 'CharField'),
        ('TextField', 'TextField'),
        ('ChoiceField', 'ChoiceField'),
        ('DateField', 'DateField'),
        ('DateTimeField', 'DateTimeField'),
        ('DecimalField', 'DecimalField')
        )
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES,
                                  null=True)
    WIDGET_TYPES = (
        ('HiddenInput', 'HiddenInput'),
        )
    widget = models.CharField(max_length=50, choices=WIDGET_TYPES,
                                  null=True, blank=True)
    possible_values = models.TextField(
        help_text="json representing key/values", null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    ftp_exportable = models.BooleanField(default=True)


    def __unicode__(self):
        return "%s - %s" % (self.type, self.description)

    class Meta:
        ordering = ['order']


class BeachVariable(models.Model):
    beach = models.ForeignKey('Beach')
    code = models.CharField(max_length=20, null=True)
    variable = models.ForeignKey('Variable', null=True)

    def __unicode__(self):
        return unicode(self.variable)

    class Meta:
        verbose_name = "Variable de playa"
        verbose_name_plural = "Variables de playa"


class SightVariables(models.Model):
    sight = models.ForeignKey('Sight')
    variable = models.ForeignKey('BeachVariable')
    value = models.FloatField()

    def __unicode__(self):
        return self.variable.variable.type

    class Meta:
        verbose_name = "Variable de avistamiento"
        verbose_name_plural = "Variables de avistamientos"


class ReportingClient(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Origen del reporte"
        verbose_name_plural = "Orígenes de reporte"
