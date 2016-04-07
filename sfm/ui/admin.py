from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin as a
from ui import models as m
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_local_id': 'This local_id has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_local_id(self):
        local_id = self.cleaned_data["local_id"]
        try:
            User.objects.get(local_id=local_id)
        except User.DoesNotExist:
            return local_id
        raise forms.ValidationError(self.error_messages['duplicate_local_id'])


@a.register(User)
class UserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm


class Credential(a.ModelAdmin):
    fields = ('user', 'platform', 'token', 'is_active', 'date_added', 'history_note')
    list_display = ['user', 'platform', 'token', 'is_active', 'date_added']
    list_filter = ['user', 'platform', 'token', 'is_active', 'date_added']
    search_fields = ['user', 'platform', 'token', 'is_active', 'date_added']


class HistoricalCredential(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'user', 'platform', 'token', 'is_active', 'date_added')
    list_display = ['user', 'platform', 'token', 'is_active', 'date_added']
    list_filter = ['user', 'platform', 'token', 'is_active', 'date_added']
    search_fields = ['user', 'platform', 'token', 'is_active', 'date_added']


class Collection(a.ModelAdmin):
    fields = ('group', 'name', 'description', 'is_visible',
              'stats', 'date_added', 'history_note')
    list_display = ['group', 'name', 'description', 'is_visible',
                    'stats', 'date_added', 'date_updated']
    list_filter = ['group', 'name', 'description', 'is_visible',
                   'stats', 'date_added', 'date_updated']
    search_fields = ['group', 'name', 'description',
                     'is_visible', 'stats', 'date_added', 'date_updated']


class HistoricalCollection(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note',  'group', 'name',
              'description', 'is_visible',
              'stats', 'date_added')
    list_display = ['group', 'name', 'description', 'is_visible',
                    'stats', 'date_added', 'date_updated']
    list_filter = ['group', 'name', 'description', 'is_visible',
                   'stats', 'date_added', 'date_updated']
    search_fields = ['group', 'name', 'description',
                     'is_visible', 'stats', 'date_added', 'date_updated']


class SeedSet(a.ModelAdmin):
    fields = ('collection', 'credential', 'harvest_type', 'name',
              'description', 'is_active', 'schedule_minutes', 'harvest_options',
              'stats', 'date_added', 'start_date', 'end_date', 'history_note')
    list_display = ['collection', 'credential', 'harvest_type', 'name',
                    'description', 'is_active', 'harvest_options',
                    'stats', 'date_added', 'start_date',
                    'end_date']
    list_filter = ['collection', 'credential', 'harvest_type', 'name',
                   'description', 'is_active', 'harvest_options',
                   'stats', 'date_added', 'start_date',
                   'end_date']
    search_fields = ['collection', 'credential', 'harvest_type', 'name',
                     'description', 'is_active',
                     'harvest_options', 'stats', 'date_added',
                     'start_date', 'end_date']


class HistoricalSeedSet(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'collection', 'credential', 'harvest_type', 'name',
              'description', 'is_active', 'schedule_minutes', 'harvest_options',
              'stats', 'date_added', 'start_date', 'end_date')
    list_display = ['collection', 'credential', 'harvest_type', 'name',
                    'description', 'is_active', 'harvest_options',
                    'stats', 'date_added', 'start_date',
                    'end_date']
    list_filter = ['collection', 'credential', 'harvest_type', 'name',
                   'description', 'is_active', 'harvest_options',
                   'stats', 'date_added', 'start_date',
                   'end_date']
    search_fields = ['collection', 'credential', 'harvest_type', 'name',
                     'description', 'is_active',
                     'harvest_options', 'stats', 'date_added',
                     'start_date', 'end_date']


class Seed(a.ModelAdmin):
    fields = ('seed_set', 'token', 'uid', 'is_active',
              'is_valid', 'stats', 'date_added', 'history_note')
    list_display = ['seed_set', 'token', 'uid', 'is_active',
                    'is_valid', 'stats', 'date_added', 'date_updated']
    list_filter = ['seed_set', 'token', 'uid', 'is_active',
                   'is_valid', 'stats', 'date_added', 'date_updated']
    search_fields = ['seed_set', 'token', 'uid', 'is_active',
                     'is_valid', 'stats', 'date_added', 'date_updated']


class HistoricalSeed(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'seed_set', 'token', 'uid', 'is_active',
              'is_valid', 'stats', 'date_added')
    list_display = ['seed_set', 'token', 'uid', 'is_active',
                    'is_valid', 'stats', 'date_added', 'date_updated']
    list_filter = ['seed_set', 'token', 'uid', 'is_active',
                   'is_valid', 'stats', 'date_added', 'date_updated']
    search_fields = ['seed_set', 'token', 'uid', 'is_active',
                     'is_valid', 'stats', 'date_added', 'date_updated']


class Harvest(a.ModelAdmin):
    fields = (
       'harvest_id', 'historical_seed_set', 'historical_seeds', 'historical_credential',
       'status', 'date_requested', 'date_started', 'date_ended', 'stats',
       'infos', 'warnings', 'errors', 'token_updates', 'uids', 'warcs_count', 'warcs_bytes')
    list_display = ['id', 'harvest_id', 'historical_seed_set', 'status', 'date_requested', 'date_updated']
    list_filter = ['status', 'date_requested', 'date_updated']
    search_fields = ['id', 'harvest_id']

a.site.register(m.Credential, Credential)
a.site.register(m.HistoricalCredential, HistoricalCredential)
a.site.register(m.Collection, Collection)
a.site.register(m.HistoricalCollection, HistoricalCollection)
a.site.register(m.SeedSet, SeedSet)
a.site.register(m.HistoricalSeedSet, HistoricalSeedSet)
a.site.register(m.Seed, Seed)
a.site.register(m.HistoricalSeed, HistoricalSeed)
a.site.register(m.Harvest, Harvest)
