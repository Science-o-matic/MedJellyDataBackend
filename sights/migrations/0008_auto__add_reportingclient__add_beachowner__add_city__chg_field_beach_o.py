# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportingClient'
        db.create_table(u'sights_reportingclient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'sights', ['ReportingClient'])

        # Adding model 'BeachOwner'
        db.create_table(u'sights_beachowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'sights', ['BeachOwner'])

        # Adding model 'City'
        db.create_table(u'sights_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'sights', ['City'])


        # Renaming column for 'Beach.owner' to match new field type.
        db.rename_column(u'sights_beach', 'owner', 'owner_id')
        # Changing field 'Beach.owner'
        db.alter_column(u'sights_beach', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.BeachOwner']))
        # Adding index on 'Beach', fields ['owner']
        db.create_index(u'sights_beach', ['owner_id'])


        # Renaming column for 'Beach.city' to match new field type.
        db.rename_column(u'sights_beach', 'city', 'city_id')
        # Changing field 'Beach.city'
        db.alter_column(u'sights_beach', 'city_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.City']))
        # Adding index on 'Beach', fields ['city']
        db.create_index(u'sights_beach', ['city_id'])

        # Adding field 'Sight.reported_from'
        db.add_column(u'sights_sight', 'reported_from',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sights.ReportingClient']),
                      keep_default=False)


    def backwards(self, orm):
        # Removing index on 'Beach', fields ['city']
        db.delete_index(u'sights_beach', ['city_id'])

        # Removing index on 'Beach', fields ['owner']
        db.delete_index(u'sights_beach', ['owner_id'])

        # Deleting model 'ReportingClient'
        db.delete_table(u'sights_reportingclient')

        # Deleting model 'BeachOwner'
        db.delete_table(u'sights_beachowner')

        # Deleting model 'City'
        db.delete_table(u'sights_city')


        # Renaming column for 'Beach.owner' to match new field type.
        db.rename_column(u'sights_beach', 'owner_id', 'owner')
        # Changing field 'Beach.owner'
        db.alter_column(u'sights_beach', 'owner', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Renaming column for 'Beach.city' to match new field type.
        db.rename_column(u'sights_beach', 'city_id', 'city')
        # Changing field 'Beach.city'
        db.alter_column(u'sights_beach', 'city', self.gf('django.db.models.fields.CharField')(max_length=1000))
        # Deleting field 'Sight.reported_from'
        db.delete_column(u'sights_sight', 'reported_from_id')


    models = {
        u'sights.beach': {
            'Meta': {'object_name': 'Beach'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.City']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.BeachOwner']"})
        },
        u'sights.beachowner': {
            'Meta': {'object_name': 'BeachOwner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.measureunit': {
            'Meta': {'object_name': 'MeasureUnit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.reportingclient': {
            'Meta': {'object_name': 'ReportingClient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.sight': {
            'Meta': {'object_name': 'Sight'},
            'beach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Beach']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reported_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.ReportingClient']"}),
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
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariablesGroup']", 'null': 'True', 'blank': 'True'}),
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