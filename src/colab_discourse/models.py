# Your models here.
from django.db import models
from django.conf import settings


class DiscourseCategory(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    text_color = models.CharField(max_length=50)
    slug = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    topic_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)


class DiscourseTopic(models.Model):

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    category = models.ForeignKey('DiscourseCategory')

    created_at = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    last_poster_username = models.CharField(max_length=255)
    last_posted_at = models.DateTimeField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name='topics')

    views = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    participant_count = models.IntegerField(default=0)

    visible = models.BooleanField(default=True)
    closed = models.BooleanField(default=False)


class DiscoursePost(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    topic = models.ForeignKey('DiscourseTopic', related_name='posts')
    post_number = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    cooked = models.TextField()

    reply_count = models.IntegerField(default=0)
    quote_count = models.IntegerField(default=0)
    reads = models.IntegerField(default=0)


class DiscourseBadgeType(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class DiscourseBadge(models.Model):

    id = models.IntegerField(primary_key=True)
    badge_type = models.ForeignKey('DiscourseBadgeType')
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    long_description = models.TextField()
    icon = models.CharField(max_length=255)
