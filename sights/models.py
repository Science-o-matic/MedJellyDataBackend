# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Sight(models.Model):
    timestamp = models.DateTimeField(verbose_name="Data de medició")
    comments = models.TextField(blank=True)
    beach = models.ForeignKey('Beach', verbose_name="Platja")
    reported_from = models.ForeignKey('ReportingClient')
    variables = models.ManyToManyField("BeachVariable", through="SightVariables")
    validated = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s (%s)" % (unicode(self.beach), self.beach.code)

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
