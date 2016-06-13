# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    replaces = [(b'colab_discourse', '0001_initial'), (b'colab_discourse', '0002_auto_20160610_1734'), (b'colab_discourse', '0003_auto_20160610_2024'), (b'colab_discourse', '0004_auto_20160613_1416')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscourseBadge',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('long_description', models.TextField()),
                ('icon', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscourseBadgeType',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscourseCategory',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=50)),
                ('text_color', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('topic_count', models.IntegerField()),
                ('post_count', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscoursePost',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('post_number', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('cooked', models.TextField()),
                ('reply_count', models.IntegerField()),
                ('quote_count', models.IntegerField()),
                ('reads', models.IntegerField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiscourseTopic',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField()),
                ('last_poster_username', models.CharField(max_length=255)),
                ('last_posted_at', models.DateTimeField()),
                ('views', models.IntegerField(default=0)),
                ('like_count', models.IntegerField(default=0)),
                ('posts_count', models.IntegerField(default=0)),
                ('participant_count', models.IntegerField(default=0)),
                ('visible', models.BooleanField(default=True)),
                ('closed', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='colab_discourse.DiscourseCategory')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='topics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='discoursepost',
            name='topic',
            field=models.ForeignKey(related_name='posts', to='colab_discourse.DiscourseTopic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='discoursebadge',
            name='badge_type',
            field=models.ForeignKey(to='colab_discourse.DiscourseBadgeType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='discoursecategory',
            name='description',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='discoursecategory',
            name='post_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='discoursecategory',
            name='topic_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='discoursepost',
            name='quote_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='discoursepost',
            name='reads',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='discoursepost',
            name='reply_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
