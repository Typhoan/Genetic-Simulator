# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab_name', models.CharField(max_length=200)),
                ('dir_name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dna_string', models.CharField(max_length=600)),
                ('name', models.CharField(max_length=200)),
                ('fileName', models.CharField(max_length=200)),
                ('lab', models.ForeignKey(to='bioedit.Lab')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
