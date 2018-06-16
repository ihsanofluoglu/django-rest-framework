# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('TaskBlogApp', '0002_auto_20160715_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_updatedAt',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_updatedAd',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
