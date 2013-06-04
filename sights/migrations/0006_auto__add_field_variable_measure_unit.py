# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Variable.measure_unit'
        db.add_column(u'sights_variable', 'measure_unit',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.MeasureUnit']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Variable.measure_unit'
        db.delete_column(u'sights_variable', 'measure_unit_id')


    models = {
        u'sights.beach': {
            'Meta': {'object_name': 'Beach'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
        },
        u'sights.measureunit': {
            'Meta': {'object_name': 'MeasureUnit'},
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariablesGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.MeasureUnit']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.variablesgroup': {
            'Meta': {'object_name': 'VariablesGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['sights']