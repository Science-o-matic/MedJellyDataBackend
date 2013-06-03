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


class VariableType(models.Model):
    beach = models.ForeignKey('Beach')
    group = models.ForeignKey('VariablesGroup')
    description = models.ForeignKey('VariableDescription')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.description)

    class Meta:
        verbose_name = "Tipo de Variable"
        verbose_name_plural = "Tipos de Variables"


class VariableDescription(models.Model):
    variable_type = models.ForeignKey('VariableType', related_name='possible_descriptions')
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Descripción de Variable"
        verbose_name_plural = "Descripciones de Variables"



class MeasureUnits(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"


class SightVariables(models.Model):
    sight = models.ForeignKey('Sight')
    variable = models.ForeignKey('VariableType')
    value = models.FloatField()

    def __unicode__(self):
        return "%s %s %s" % (self.sight, self.variable, self.value)


    class Meta:
        verbose_name = "Variable de avistamiento"
        verbose_name_plural = "Variables de avistamientos"
