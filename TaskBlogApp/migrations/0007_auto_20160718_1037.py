# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('TaskBlogApp', '0006_auto_20160718_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
