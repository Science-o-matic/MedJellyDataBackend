# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sight'
        db.create_table(u'sights_sight', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('beach', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.Beach'])),
        ))
        db.send_create_signal(u'sights', ['Sight'])

        # Adding model 'Beach'
        db.create_table(u'sights_beach', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['Beach'])

        # Adding model 'VariablesGroup'
        db.create_table(u'sights_variablesgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['VariablesGroup'])

        # Adding model 'VariableType'
        db.create_table(u'sights_variabletype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beach', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.Beach'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariablesGroup'])),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariableDescription'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['VariableType'])

        # Adding model 'VariableDescription'
        db.create_table(u'sights_variabledescription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variable_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='possible_descriptions', to=orm['sights.VariableType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['VariableDescription'])

        # Adding model 'MeasureUnits'
        db.create_table(u'sights_measureunits', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['MeasureUnits'])

        # Adding model 'SightVariables'
        db.create_table(u'sights_sightvariables', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sight', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.Sight'])),
            ('variable', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariableType'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'sights', ['SightVariables'])


    def backwards(self, orm):
        # Deleting model 'Sight'
        db.delete_table(u'sights_sight')

        # Deleting model 'Beach'
        db.delete_table(u'sights_beach')

        # Deleting model 'VariablesGroup'
        db.delete_table(u'sights_variablesgroup')

        # Deleting model 'VariableType'
        db.delete_table(u'sights_variabletype')

        # Deleting model 'VariableDescription'
        db.delete_table(u'sights_variabledescription')

        # Deleting model 'MeasureUnits'
        db.delete_table(u'sights_measureunits')

        # Deleting model 'SightVariables'
        db.delete_table(u'sights_sightvariables')


    models = {
        u'sights.beach': {
            'Meta': {'object_name': 'Beach'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.measureunits': {
            'Meta': {'object_name': 'MeasureUnits'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.sight': {
            'Meta': {'object_name': 'Sight'},
            'beach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Beach']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'sights.sightvariables': {
            'Meta': {'object_name': 'SightVariables'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sight': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Sight']"}),
            'value': ('django.db.models.fields.FloatField', [], {}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariableType']"})
        },
        u'sights.variabledescription': {
            'Meta': {'object_name': 'VariableDescription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'variable_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'possible_descriptions'", 'to': u"orm['sights.VariableType']"})
        },
        u'sights.variablesgroup': {
            'Meta': {'object_name': 'VariablesGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.variabletype': {
            'Meta': {'object_name': 'VariableType'},
            'beach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Beach']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariableDescription']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariablesGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['sights']