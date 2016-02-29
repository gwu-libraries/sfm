from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


class User(AbstractUser):

    local_id = models.CharField(max_length=255, blank=True, default='',
                                help_text='Local identifier')


class Credential(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'twitter'),
        ('flickr', 'flickr'),
        ('weibo', 'weibo'),
        ('tumblr', 'tumblr')
    ]
    user = models.ForeignKey(User, related_name='credentials')
    platform = models.CharField(max_length=255, choices=PLATFORM_CHOICES)
    token = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<Credential %s "%s">' % (self.platform, self.token)


@python_2_unicode_compatible
class Collection(models.Model):

    group = models.ForeignKey(Group, related_name='collections')
    name = models.CharField(max_length=255, blank=False,
                            verbose_name='Collection name')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Collection %s "%s">' % (self.id, self.name)


@python_2_unicode_compatible
class SeedSet(models.Model):
    SCHEDULE_CHOICES = [
        (60, 'Every hour'),
        (60 * 24, 'Every day'),
        (60 * 24 * 7, 'Every week'),
        (60 * 24 * 7 * 4, 'Every 4 weeks')
    ]
    HARVEST_CHOICES = [
        ('twitter_search', 'Twitter search'),
        ('twitter_filter', 'Twitter filter'),
        ('flickr_user', 'Flickr user')
    ]
    collection = models.ForeignKey(Collection, related_name='seed_sets')
    credential = models.ForeignKey(Credential, related_name='seed_sets')
    harvest_type = models.CharField(max_length=255, choices=HARVEST_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    schedule_minutes = models.PositiveIntegerField(default=60 * 24 * 7, choices=SCHEDULE_CHOICES,
                                                   verbose_name="schedule")
    harvest_options = models.TextField(blank=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(blank=True,
                                      null=True,
                                      help_text="If blank, will start now.")
    end_date = models.DateTimeField(blank=True,
                                    null=True,
                                    help_text="If blank, will continue until stopped.")

    def __str__(self):
        return '<SeedSet %s "%s">' % (self.id, self.name)


@python_2_unicode_compatible
class Seed(models.Model):

    seed_set = models.ForeignKey(SeedSet, related_name='seeds')
    token = models.TextField(blank=True)
    uid = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Seed %s "%s">' % (self.id, self.token)


class Harvest(models.Model):
    REQUESTED = "requested"
    SUCCESS = "completed success"
    FAILURE = "completed failure"
    RUNNING = "running"
    STATUS_CHOICES = (
        (REQUESTED, REQUESTED),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
        (RUNNING, RUNNING)
    )
    seed_set = models.ForeignKey(SeedSet, related_name='harvests')
    harvest_id = models.CharField(max_length=255, blank=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    date_requested = models.DateTimeField(blank=True, default=timezone.now)
    date_started = models.DateTimeField(blank=True, null=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    stats = JSONField(blank=True)
    infos = JSONField(blank=True)
    warnings = JSONField(blank=True)
    errors = JSONField(blank=True)
    token_updates = JSONField(blank=True)
    uids = JSONField(blank=True)
    warcs_count = models.PositiveIntegerField(default=0)
    warcs_bytes = models.BigIntegerField(default=0)


class Media(models.Model):

    harvest = models.ForeignKey(Harvest, related_name='media')
    size = models.PositiveIntegerField(default=0, help_text='Size (bytes)')
    host = models.CharField(max_length=255, blank=True)
    path = models.TextField(blank=True)
