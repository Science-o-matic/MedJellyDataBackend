# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'VariableType'
        db.delete_table(u'sights_variabletype')

        # Deleting model 'VariableDescription'
        db.delete_table(u'sights_variabledescription')

        # Adding model 'Variable'
        db.create_table(u'sights_variable', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beach', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.Beach'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariablesGroup'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['Variable'])


        # Changing field 'SightVariables.variable'
        db.alter_column(u'sights_sightvariables', 'variable_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.Variable']))

    def backwards(self, orm):
        # Adding model 'VariableType'
        db.create_table(u'sights_variabletype', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariablesGroup'])),
            ('description', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariableDescription'])),
            ('beach', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.Beach'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['VariableType'])

        # Adding model 'VariableDescription'
        db.create_table(u'sights_variabledescription', (
            ('variable_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='possible_descriptions', to=orm['sights.VariableType'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'sights', ['VariableDescription'])

        # Deleting model 'Variable'
        db.delete_table(u'sights_variable')


        # Changing field 'SightVariables.variable'
        db.alter_column(u'sights_sightvariables', 'variable_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.VariableType']))

    models = {
        u'sights.beach': {
            'Meta': {'object_name': 'Beach'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
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
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Variable']"})
        },
        u'sights.variable': {
            'Meta': {'object_name': 'Variable'},
            'beach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Beach']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariablesGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.variablesgroup': {
            'Meta': {'object_name': 'VariablesGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['sights']