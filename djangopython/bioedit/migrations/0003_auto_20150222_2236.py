# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bioedit', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='spefile',
            field=models.FileField(upload_to='documents'),
            preserve_default=True,
        ),
    ]
