# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dnaedit', '0002_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=200)),
                ('datetime_uploaded', models.DateTimeField()),
                ('datetime_timezone', models.CharField(max_length=200)),
                ('lab', models.ForeignKey(to='dnaedit.Lab')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='species',
            name='lab',
        ),
        migrations.AlterField(
            model_name='species',
            name='fileName',
            field=models.ForeignKey(to='dnaedit.LabFile'),
            preserve_default=True,
        ),
    ]
