# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.models import User
from sights.exporters import FTPExporter, APIExporter


class Sight(models.Model):
    timestamp = models.DateTimeField(verbose_name="Data de medició")
    comments = models.TextField(blank=True)
    beach = models.ForeignKey('Beach', verbose_name="Platja")
    reported_from = models.ForeignKey('ReportingClient')
    variables = models.ManyToManyField("BeachVariable", through="SightVariables")
    validated = models.BooleanField(default=False, verbose_name="Validat")
    api_sent = models.BooleanField(default=False, verbose_name="Enviat per API")
    api_sent_timestamp = models.DateTimeField(verbose_name="Data de enviament per API", null=True, blank=True)
    ftp_sent = models.BooleanField(default=False, verbose_name="Enviat per FTP")
    ftp_sent_timestamp = models.DateTimeField(verbose_name="Data de enviament per FTP", null=True, blank=True)


    JELLYFISH_STATUS = {
        (0, 0): "NO_WARNING",
        (1, 7): "LOW_WARNING",
        (8, 12): "HIGH_WARNING",
        (13, 13): "VERY_HIGH_WARNING"
    }


    def __unicode__(self):
        return u"%s (%s)" % (unicode(self.beach), self.beach.code)

    def export(self):
        if self.validated and not self.sent:
            # Temporary disabled
            # FTPExporter(self).export()
            APIExporter(self).export()
            self.api_sent = True
            self.api_sent_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%I")
            self.save()

    def get_flag(self):
        try:
            return self.sightvariables_set.filter(variable__variable__api_export_id=0)[0].value
        except IndexError:
            return 0 # NO_INFO

    def get_flag_reason(self):
        try:
            return self.sightvariables_set.filter(variable__variable__api_export_id=99)[0].value
        except IndexError:
            return '' # NOT VERIFIED

    def get_jellyFishStatus(self):
        try:
            qs = self.sightvariables_set.exclude(variable__variable__api_export_id=None)
            warning_level = self.max_warning_level(qs)
            return self._jellyFishStatus(warning_level)
        except IndexError:
            return 0 # NONE

    def max_warning_level(self, qs):
        max_level = 0
        # Value = 1 indicates presence
        for var in qs.filter(value=1):
            warning_level = var.variable.variable.api_warning_level
            if warning_level > max_level:
                max_level = warning_level
        return max_level


    def _jellyFishStatus(self, warning_level):
        for k, v in self.JELLYFISH_STATUS.items():
            if (warning_level >= k[0]) and (warning_level <= k[1]):
                return v

    class Meta:
        verbose_name = "Avistamiento"


class Beach(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=1000)
    city = models.ForeignKey("City")
    owner = models.ForeignKey("BeachOwner")
    users = models.ManyToManyField(User)
    api_id = models.IntegerField(null=True, blank=False)

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
    api_export_id = models.IntegerField(null=True, blank=True)
    api_warning_level = models.IntegerField(null=True, blank=True)

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
    value = models.DecimalField(max_digits=6, decimal_places=2)

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
