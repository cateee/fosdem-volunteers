# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Talk.meeting'
        db.add_column('volunteers_talk', 'meeting',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['schedule.Meeting'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field meeting on 'Talk'
        db.delete_table(db.shorten_name('volunteers_talk_meeting'))


    def backwards(self, orm):
        # Deleting field 'Talk.meeting'
        db.delete_column('volunteers_talk', 'meeting_id')

        # Adding M2M table for field meeting on 'Talk'
        m2m_table_name = db.shorten_name('volunteers_talk_meeting')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm['volunteers.talk'], null=False)),
            ('meeting', models.ForeignKey(orm['schedule.meeting'], null=False))
        ))
        db.create_unique(m2m_table_name, ['talk_id', 'meeting_id'])


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
        'schedule.attendee': {
            'Meta': {'ordering': "('user__username', 'summit')", 'object_name': 'Attendee'},
            'crew': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'crew'"}),
            'end_utc': ('django.db.models.fields.DateTimeField', [], {'db_column': "'end'"}),
            'from_launchpad': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'secret_key_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'start_utc': ('django.db.models.fields.DateTimeField', [], {'db_column': "'start'"}),
            'summit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Summit']"}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['schedule.Track']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'schedule.eventtype': {
            'Meta': {'ordering': "('name', 'summit')", 'object_name': 'EventType'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'FFFFFF'", 'max_length': '6'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'note': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'plural': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'selectable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'summit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Summit']"})
        },
        'schedule.meeting': {
            'Meta': {'object_name': 'Meeting'},
            'approved': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '10', 'null': 'True'}),
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'approver_set'", 'null': 'True', 'to': "orm['schedule.Attendee']"}),
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assignee_set'", 'null': 'True', 'to': "orm['schedule.Attendee']"}),
            'broadcast_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2047'}),
            'drafter': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'drafter_set'", 'null': 'True', 'to': "orm['schedule.Attendee']"}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'45 min'", 'max_length': '10', 'blank': 'True'}),
            'eventtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.EventType']"}),
            'hangout_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launchpad_blueprint_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('summit.schedule.fields.NameField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '2047', 'null': 'True', 'blank': 'True'}),
            'override_break': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pad_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'participants': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['schedule.Attendee']", 'symmetrical': 'False', 'through': "orm['schedule.Participant']", 'blank': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'private_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'requires_dial_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scribe': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scribe_set'", 'null': 'True', 'to': "orm['schedule.Attendee']"}),
            'slots': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'speaker_set'", 'blank': 'True', 'to': "orm['schedule.Attendee']"}),
            'spec_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'summit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Summit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tracks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['schedule.Track']", 'symmetrical': 'False', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "u'discussion'", 'max_length': '15'}),
            'urls': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'virtual_meeting': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wiki_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'schedule.participant': {
            'Meta': {'ordering': "('meeting', 'attendee', 'participation')", 'object_name': 'Participant'},
            'attendee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Attendee']"}),
            'from_launchpad': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Meeting']"}),
            'participation': ('django.db.models.fields.CharField', [], {'default': "'ATTENDING'", 'max_length': '32', 'null': 'True'})
        },
        'schedule.summit': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Summit'},
            'date_arrival': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_arrival_staff': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_departure': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_departure_staff': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2047', 'blank': 'True'}),
            'etherpad': ('django.db.models.fields.URLField', [], {'default': "'http://pad.ubuntu.com/'", 'max_length': '75'}),
            'hashtag': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'managers'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'name': ('summit.schedule.fields.NameField', [], {'max_length': '50'}),
            'qr': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'schedulers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'schedulers'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'social_media': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'setup'", 'max_length': '20'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'virtual_summit': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'schedule.track': {
            'Meta': {'ordering': "('summit', 'title', 'slug')", 'object_name': 'Track'},
            'allow_adjacent_sessions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'FFFFFF'", 'max_length': '6'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'summit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Summit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'meeting': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Meeting']", 'null': 'True', 'blank': 'True'}),
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