# -*- coding: utf-8 -*-
import json
import datetime
from django.db import models
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.models import User
from sights.exporters import APIExporter


class Sight(models.Model):
    timestamp = models.DateTimeField(verbose_name="Data de medició")
    comments = models.TextField(blank=True)
    beach = models.ForeignKey('Beach', verbose_name="Platja")
    reported_from = models.ForeignKey('ReportingClient', verbose_name="Reportat per")
    validated = models.BooleanField(default=False, verbose_name="Validat")
    api_sent = models.BooleanField(default=False, verbose_name="Enviat per API")
    api_sent_timestamp = models.DateTimeField(verbose_name="Data de enviament per API", null=True, blank=True)
    # TODO: Next two fields can be dropped
    ftp_sent = models.BooleanField(default=False, verbose_name="Enviat per FTP")
    ftp_sent_timestamp = models.DateTimeField(verbose_name="Data de enviament per FTP", null=True, blank=True)
    jellyfishes_presence = models.BooleanField(default=False, verbose_name="Presencia de medusas")

    JELLYFISH_STATUS = {
        (0, 0): "NO_WARNING",
        (1, 7): "LOW_WARNING",
        (8, 12): "HIGH_WARNING",
        (13, 13): "VERY_HIGH_WARNING"
    }

    class Meta:
        verbose_name = "Avistamiento"

    def __unicode__(self):
        return u"[%s] %s" % (self.timestamp, unicode(self.beach))

    def save(self, *args, **kwargs):
        self.jellyfishes_presence = bool(self.jellyfishes.count())
        super(Sight, self).save(*args, **kwargs)

    def export(self):
        if self.validated and not self.api_sent:
            APIExporter(self).export()
            self.api_sent = True
            self.api_sent_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save()

    def get_flag(self):
        try:
            return self.variables.filter(variable__api_export_id=0)[0].value
        except IndexError:
            return 0 # NO_INFO

    def get_flag_reason(self):
        try:
            value = self.variables.filter(variable__api_export_id=99)[0].value
            if value == 15:
                value = ''
            else:
                value = int(value)
        except IndexError:
            value = ''
        return value

    def get_jellyFishStatus(self):
        try:
            qs = self.variables.exclude(variable__api_export_id=None)
            warning_level = self._max_warning_level(qs)
            return self._jellyFishStatus(warning_level)
        except IndexError:
            return 0 # NONE

    def _max_warning_level(self, qs):
        max_level = 0
        # Value = 1 indicates presence
        for var in qs.filter(value=1):
            warning_level = var.variable.api_warning_level
            if warning_level > max_level:
                max_level = warning_level
        return max_level

    def get_variables_by_group_name(self, group_name):
        return self.sightvariables_set.filter(variable__group__name=group_name,
                                              value=True)
    def get_variable_by_type(self, variable_type):
        return self.sightvariables_set.get(variable__type=variable_type)

    def get_water_temp(self):
        return round(self.variables.get(variable_id=63).value, 2)

    def _jellyFishStatus(self, warning_level):
        for k, v in self.JELLYFISH_STATUS.items():
            if (warning_level >= k[0]) and (warning_level <= k[1]):
                return v




class Jellyfish(models.Model):
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    medjelly_api_id = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Jellyfishes"

    def __unicode__(self):
        return self.name



class JellyfishAbundance(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class JellyfishSize(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Beach(models.Model):
    name = models.CharField(max_length=1000)
    city = models.ForeignKey("City")
    owner = models.ForeignKey("BeachOwner")
    users = models.ManyToManyField(User)
    medjelly_api_id = models.IntegerField(null=True, blank=True)
    proteccion_civil_api_id = models.CharField(max_length=300, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Playa"


class City(models.Model):
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Ayuntamiento"
        verbose_name_plural = "Ayuntamientos"


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
                                     default=MeasureUnit.get_default)
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
    DEFAULT_BOOLEAN_FIELD_VALUE = 2
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES,
                                  null=True)
    WIDGET_TYPES = (
        ('HiddenInput', 'HiddenInput'),
        )
    widget = models.CharField(max_length=50, choices=WIDGET_TYPES,
                              null=True, blank=True)
    possible_values = models.TextField(help_text="json representing key/values",
                                       null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    api_export_id = models.IntegerField(null=True, blank=True)
    api_warning_level = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.type, self.description)

    class Meta:
        ordering = ['order']


class SightJellyfishes(models.Model):
    sight = models.ForeignKey('Sight', related_name="jellyfishes")
    jellyfish = models.ForeignKey('Jellyfish', related_name="sightings")
    size = models.ForeignKey('JellyfishSize')
    abundance = models.ForeignKey('JellyfishAbundance')


class SightVariables(models.Model):
    sight = models.ForeignKey('Sight', related_name="variables")
    variable = models.ForeignKey('Variable')
    value = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        repr_string = self.variable.type
        if self.variable.possible_values:
            values = json.loads(self.variable.possible_values)
            repr_string += ' ('
            for v in values:
                repr_string += "%s = %s, " % (v[0], v[1])
            repr_string += ')'
        return repr_string

    class Meta:
        verbose_name = "Variable de avistamiento"
        verbose_name_plural = "Variables de avistamientos"


class ReportingClient(models.Model):
    name = models.CharField(max_length=300)
    last_import_date = models.DateTimeField(null=True, blank=True)
    # TODO: this field could probably be deprecated:
    code = models.CharField(max_length=300, blank=True, null=True)


    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Origen del reporte"
        verbose_name_plural = "Orígenes de reporte"


class ProteccionCivilBeach(models.Model):
    """
    This model is used as a reference during the process of
    putting together the Beach model data from different source.
    It's holding beaches from Proteccion Civíl's API
    """
    code = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    town = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Playa (Protección Civíl)"
        verbose_name_plural = "Playas (Protección Civíl)"


    def __unicode__(self):
        return self.name


class MedJellyBeach(models.Model):
    """
    This model is used as a reference during the process of
    putting together the Beach model data from different sources.
    It's holding beaches from MedJelly's API
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    town = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Playa (MedJelly)"
        verbose_name_plural = "Playas (MedJelly)"

    def __unicode__(self):
        return self.name
