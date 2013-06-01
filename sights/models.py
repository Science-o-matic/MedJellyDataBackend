from django.db import models
from django.db import models


class Sight(models.Model):
    timestamp = models.DateTimeField()
    comments = models.TextField(blank=True)
    beach = models.ForeignKey('Beach')

    def __unicode__(self):
        return "%s: %s (%s)" % (self.timestamp, self.beach, self.beach_code)


class Beach(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class VariablesGroup(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class VariableType(models.Model):
    beach = models.ForeignKey('Beach')
    group = models.ForeignKey('VariablesGroup')
    description = models.ForeignKey('VariableDescription')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.description)


class VariableDescription(models.Model):
    variable_type = models.ForeignKey('VariableType', related_name='possible_descriptions')
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class MeasureUnits(models.Model):
    name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.name


class SightVariables(models.Model):
    sight = models.ForeignKey('Sight')
    variable = models.ForeignKey('VariableType')
    value = models.FloatField()

    def __unicode__(self):
        return "%s %s %s" % (self.sight, self.variable, self.value)
