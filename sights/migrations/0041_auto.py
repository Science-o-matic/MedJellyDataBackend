# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field proteccion_civil_beaches on 'Beach'
        m2m_table_name = db.shorten_name(u'sights_beach_proteccion_civil_beaches')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('beach', models.ForeignKey(orm[u'sights.beach'], null=False)),
            ('proteccioncivilbeach', models.ForeignKey(orm[u'sights.proteccioncivilbeach'], null=False))
        ))
        db.create_unique(m2m_table_name, ['beach_id', 'proteccioncivilbeach_id'])


    def backwards(self, orm):
        # Removing M2M table for field proteccion_civil_beaches on 'Beach'
        db.delete_table(db.shorten_name(u'sights_beach_proteccion_civil_beaches'))


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
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medjelly_api_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sights.BeachOwner']"}),
            'proteccion_civil_api_id': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'proteccion_civil_beaches': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sights.ProteccionCivilBeach']", 'symmetrical': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'sights.beachowner': {
            'Meta': {'object_name': 'BeachOwner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
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
        u'sights.medjellybeach': {
            'Meta': {'object_name': 'MedJellyBeach'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.proteccioncivilbeach': {
            'Meta': {'object_name': 'ProteccionCivilBeach'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'sights.reportingclient': {
            'Meta': {'object_name': 'ReportingClient'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_import_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'jellyfishes_presence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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