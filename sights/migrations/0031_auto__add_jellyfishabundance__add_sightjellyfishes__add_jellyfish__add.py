# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JellyfishAbundance'
        db.create_table(u'sights_jellyfishabundance', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'sights', ['JellyfishAbundance'])

        # Adding model 'SightJellyfishes'
        db.create_table(u'sights_sightjellyfishes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sight', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jellyfishes', to=orm['sights.Sight'])),
            ('jellyfish', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sightings', to=orm['sights.Jellyfish'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.JellyfishSize'])),
            ('abundance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sights.JellyfishAbundance'])),
        ))
        db.send_create_signal(u'sights', ['SightJellyfishes'])

        # Adding model 'Jellyfish'
        db.create_table(u'sights_jellyfish', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('medjelly_api_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'sights', ['Jellyfish'])

        # Adding model 'JellyfishSize'
        db.create_table(u'sights_jellyfishsize', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'sights', ['JellyfishSize'])


    def backwards(self, orm):
        # Deleting model 'JellyfishAbundance'
        db.delete_table(u'sights_jellyfishabundance')

        # Deleting model 'SightJellyfishes'
        db.delete_table(u'sights_sightjellyfishes')

        # Deleting model 'Jellyfish'
        db.delete_table(u'sights_jellyfish')

        # Deleting model 'JellyfishSize'
        db.delete_table(u'sights_jellyfishsize')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sights.beach': {
            'Meta': {'object_name': 'Beach'},
            'api_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.City']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.BeachOwner']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
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
        u'sights.jellyfish': {
            'Meta': {'object_name': 'Jellyfish'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medjelly_api_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.jellyfishabundance': {
            'Meta': {'object_name': 'JellyfishAbundance'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sights.jellyfishsize': {
            'Meta': {'object_name': 'JellyfishSize'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sights.measureunit': {
            'Meta': {'object_name': 'MeasureUnit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'sights.reportingclient': {
            'Meta': {'object_name': 'ReportingClient'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.sight': {
            'Meta': {'object_name': 'Sight'},
            'api_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'api_sent_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'beach': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Beach']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ftp_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ftp_sent_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reported_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.ReportingClient']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sights.sightjellyfishes': {
            'Meta': {'object_name': 'SightJellyfishes'},
            'abundance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.JellyfishAbundance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jellyfish': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sightings'", 'to': u"orm['sights.Jellyfish']"}),
            'sight': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jellyfishes'", 'to': u"orm['sights.Sight']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.JellyfishSize']"})
        },
        u'sights.sightvariables': {
            'Meta': {'object_name': 'SightVariables'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sight': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variables'", 'to': u"orm['sights.Sight']"}),
            'value': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.Variable']"})
        },
        u'sights.variable': {
            'Meta': {'ordering': "['order']", 'object_name': 'Variable'},
            'api_export_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'api_warning_level': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.VariablesGroup']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'measure_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.MeasureUnit']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'possible_values': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'widget': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'sights.variablesgroup': {
            'Meta': {'object_name': 'VariablesGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['sights']