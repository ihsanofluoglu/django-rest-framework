# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskBlogApp', '0007_auto_20160718_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='author',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
