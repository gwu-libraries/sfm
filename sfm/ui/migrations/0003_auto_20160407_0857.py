# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0002_auto_20160407_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalcredential',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
