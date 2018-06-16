# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskBlogApp', '0004_auto_20160715_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(),
        ),
    ]
