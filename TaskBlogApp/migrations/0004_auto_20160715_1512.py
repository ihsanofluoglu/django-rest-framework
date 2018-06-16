# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskBlogApp', '0003_auto_20160715_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_createdAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_createdAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
