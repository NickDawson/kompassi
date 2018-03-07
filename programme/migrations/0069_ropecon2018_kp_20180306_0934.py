# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-06 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0068_auto_20180305_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='ropecon2018_kp_difficulty',
            field=models.CharField(choices=[('simple', 'Simple'), ('advanced', 'Advanced'), ('high', 'Highly Advanced')], default='simple', max_length=15, null=True, verbose_name='Game difficulty and complexity'),
        ),
        migrations.AddField(
            model_name='programme',
            name='ropecon2018_kp_length',
            field=models.CharField(choices=[('4h', '4 hours'), ('8h', '8 hours')], default='4h', help_text='Presenters get a weekend ticket for 8 hours of presenting or a day ticket for 4 hours.', max_length=2, null=True, verbose_name='How long do you present your game'),
        ),
        migrations.AddField(
            model_name='programme',
            name='ropecon2018_kp_tables',
            field=models.CharField(choices=[('1', '1 table'), ('2', '2 tables'), ('3', '3 tables'), ('4+', '4+ tables')], default='1', help_text='Table size is about 140 x 80 cm.', max_length=5, null=True, verbose_name='How many tables do you need'),
        ),
    ]
