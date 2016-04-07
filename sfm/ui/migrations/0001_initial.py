# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields
import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('local_id', models.CharField(default=b'', help_text=b'Local identifier', max_length=255, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Collection name')),
                ('description', models.TextField(blank=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('stats', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('history_note', models.TextField(blank=True)),
                ('group', models.ForeignKey(related_name='collections', to='auth.Group')),
            ],
            options={
                'diff_fields': ('group', 'name', 'description', 'is_active'),
            },
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('platform', models.CharField(help_text=b'Platform name', max_length=255, blank=True)),
                ('token', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('history_note', models.TextField(blank=True)),
                ('user', models.ForeignKey(related_name='credentials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'diff_fields': ('platform', 'token', 'is_active'),
            },
        ),
        migrations.CreateModel(
            name='Harvest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('harvest_id', models.CharField(unique=True, max_length=255)),
                ('status', models.CharField(default=b'requested', max_length=20, choices=[(b'requested', b'requested'), (b'completed success', b'completed success'), (b'completed failure', b'completed failure'), (b'running', b'running')])),
                ('date_requested', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('date_started', models.DateTimeField(null=True, blank=True)),
                ('date_ended', models.DateTimeField(null=True, blank=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('stats', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('infos', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('warnings', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('errors', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('token_updates', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('uids', jsonfield.fields.JSONField(default=dict, blank=True)),
                ('warcs_count', models.PositiveIntegerField(default=0)),
                ('warcs_bytes', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCollection',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Collection name')),
                ('description', models.TextField(blank=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('stats', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(editable=False, blank=True)),
                ('history_note', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('group', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='auth.Group', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical collection',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCredential',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('platform', models.CharField(help_text=b'Platform name', max_length=255, blank=True)),
                ('token', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(editable=False, blank=True)),
                ('history_note', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical credential',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSeed',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('token', models.TextField(blank=True)),
                ('uid', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('stats', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(editable=False, blank=True)),
                ('history_note', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical seed',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSeedSet',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('harvest_type', models.CharField(max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'flickr_user', b'Flickr user')])),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('schedule_minutes', models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')])),
                ('harvest_options', models.TextField(blank=True)),
                ('stats', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(editable=False, blank=True)),
                ('start_date', models.DateTimeField(help_text=b'If blank, will start now.', null=True, blank=True)),
                ('end_date', models.DateTimeField(help_text=b'If blank, will continue until stopped.', null=True, blank=True)),
                ('history_note', models.TextField(blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('collection', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='ui.Collection', null=True)),
                ('credential', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='ui.Credential', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical seed set',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.PositiveIntegerField(default=0, help_text=b'Size (bytes)')),
                ('host', models.CharField(max_length=255, blank=True)),
                ('path', models.TextField(blank=True)),
                ('harvest', models.ForeignKey(related_name='media', to='ui.Harvest')),
            ],
        ),
        migrations.CreateModel(
            name='Seed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.TextField(blank=True)),
                ('uid', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('stats', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('history_note', models.TextField(blank=True)),
            ],
            options={
                'diff_fields': ('token', 'uid', 'is_active'),
            },
        ),
        migrations.CreateModel(
            name='SeedSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('harvest_type', models.CharField(max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'flickr_user', b'Flickr user')])),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('schedule_minutes', models.PositiveIntegerField(default=10080, verbose_name=b'schedule', choices=[(60, b'Every hour'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')])),
                ('harvest_options', models.TextField(blank=True)),
                ('stats', models.TextField(blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(help_text=b'If blank, will start now.', null=True, blank=True)),
                ('end_date', models.DateTimeField(help_text=b'If blank, will continue until stopped.', null=True, blank=True)),
                ('history_note', models.TextField(blank=True)),
                ('collection', models.ForeignKey(related_name='seed_sets', to='ui.Collection')),
                ('credential', models.ForeignKey(related_name='seed_sets', to='ui.Credential')),
            ],
            options={
                'diff_fields': ('collection', 'credential', 'harvest_type', 'name', 'description', 'is_active', 'schedule_minutes', 'harvest_options', 'start_date', 'end_date'),
            },
        ),
        migrations.AddField(
            model_name='seed',
            name='seed_set',
            field=models.ForeignKey(related_name='seeds', to='ui.SeedSet'),
        ),
        migrations.AddField(
            model_name='historicalseed',
            name='seed_set',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='ui.SeedSet', null=True),
        ),
        migrations.AddField(
            model_name='harvest',
            name='historical_credential',
            field=models.ForeignKey(related_name='historical_harvests', to='ui.HistoricalCredential'),
        ),
        migrations.AddField(
            model_name='harvest',
            name='historical_seed_set',
            field=models.ForeignKey(related_name='historical_harvests', to='ui.HistoricalSeedSet'),
        ),
        migrations.AddField(
            model_name='harvest',
            name='historical_seeds',
            field=models.ManyToManyField(related_name='historical_harvests', to='ui.HistoricalSeed'),
        ),
    ]
