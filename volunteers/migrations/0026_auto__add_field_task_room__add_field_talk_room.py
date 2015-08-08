# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Task.room'
        db.add_column('volunteers_task', 'room',
                      self.gf('django.db.models.fields.CharField')(default='somewhere', max_length=128),
                      keep_default=False)

        # Adding field 'Talk.room'
        db.add_column('volunteers_talk', 'room',
                      self.gf('django.db.models.fields.CharField')(default='somewhere', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Task.room'
        db.delete_column('volunteers_task', 'room')

        # Deleting field 'Talk.room'
        db.delete_column('volunteers_talk', 'room')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'ordering': "['username']", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'volunteers.edition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Edition'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'visible_from': ('django.db.models.fields.DateField', [], {}),
            'visible_until': ('django.db.models.fields.DateField', [], {})
        },
        'volunteers.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'volunteers.talk': {
            'Meta': {'ordering': "['date', 'start_time', '-end_time', 'title']", 'object_name': 'Talk'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'ext_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'default': "'somewhere'", 'max_length': '128'}),
            'speaker': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Track']"}),
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.Volunteer']", 'null': 'True', 'through': "orm['volunteers.VolunteerTalk']", 'blank': 'True'})
        },
        'volunteers.task': {
            'Meta': {'ordering': "['date', 'start_time', '-end_time', 'name']", 'object_name': 'Task'},
            'counter': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'default': 'False', 'to': "orm['volunteers.Edition']"}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'nbr_volunteers': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_volunteers_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nbr_volunteers_min': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'room': ('django.db.models.fields.CharField', [], {'default': "'somewhere'", 'max_length': '128'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Talk']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.TaskTemplate']"}),
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.Volunteer']", 'null': 'True', 'through': "orm['volunteers.VolunteerTask']", 'blank': 'True'})
        },
        'volunteers.taskcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'TaskCategory'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.Volunteer']", 'null': 'True', 'through': "orm['volunteers.VolunteerCategory']", 'blank': 'True'})
        },
        'volunteers.tasktemplate': {
            'Meta': {'ordering': "['name']", 'object_name': 'TaskTemplate'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.TaskCategory']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'volunteers.track': {
            'Meta': {'ordering': "['date', 'start_time', 'title']", 'object_name': 'Track'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'default': 'False', 'to': "orm['volunteers.Edition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'volunteers.volunteer': {
            'Meta': {'ordering': "['user__first_name', 'user__last_name']", 'object_name': 'Volunteer'},
            'about_me': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.TaskCategory']", 'null': 'True', 'through': "orm['volunteers.VolunteerCategory']", 'blank': 'True'}),
            'editions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.Edition']", 'null': 'True', 'through': "orm['volunteers.VolunteerStatus']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'mobile_nbr': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'private_staff_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'private_staff_rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'signed_up': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['volunteers.Task']", 'null': 'True', 'through': "orm['volunteers.VolunteerTask']", 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'volunteer'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'volunteers.volunteercategory': {
            'Meta': {'object_name': 'VolunteerCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.TaskCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Volunteer']"})
        },
        'volunteers.volunteerlanguage': {
            'Meta': {'object_name': 'VolunteerLanguage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Language']"}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Volunteer']"})
        },
        'volunteers.volunteerstatus': {
            'Meta': {'object_name': 'VolunteerStatus'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edition': ('django.db.models.fields.related.ForeignKey', [], {'default': 'False', 'to': "orm['volunteers.Edition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Volunteer']"})
        },
        'volunteers.volunteertalk': {
            'Meta': {'object_name': 'VolunteerTalk'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Talk']"}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Volunteer']"})
        },
        'volunteers.volunteertask': {
            'Meta': {'object_name': 'VolunteerTask'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Task']"}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['volunteers.Volunteer']"})
        }
    }

    complete_apps = ['volunteers']