# -*- coding: utf-8 -*-

from django.db import models
from django.db import models


class Sight(models.Model):
    timestamp = models.DateTimeField()
    comments = models.TextField(blank=True)
    beach = models.ForeignKey('Beach')

    def __unicode__(self):
        return "%s: %s (%s)" % (self.timestamp, self.beach, self.beach_code)

    class Meta:
        verbose_name = "Avistamiento"


class Beach(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000, blank=True)
    owner = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Playa"


class VariablesGroup(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name

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
    beach = models.ForeignKey('Beach')
    group = models.ForeignKey('VariablesGroup', null=True, blank=True)
    code = models.CharField(max_length=20)
    type = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    measure_unit = models.ForeignKey('MeasureUnit',
                                     default = MeasureUnit.get_default)

    def __unicode__(self):
        return "%s - %s" % (self.type, self.description)

    class Meta:
        verbose_name = "Variable"
        verbose_name_plural = "Variables"


class SightVariables(models.Model):
    sight = models.ForeignKey('Sight')
    variable = models.ForeignKey('Variable')
    value = models.FloatField()

    def __unicode__(self):
        return "%s %s %s" % (self.sight, self.variable, self.value)

    class Meta:
        verbose_name = "Variable de avistamiento"
        verbose_name_plural = "Variables de avistamientos"
