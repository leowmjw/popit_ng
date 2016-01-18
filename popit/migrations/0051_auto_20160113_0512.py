# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-13 05:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0050_auto_20151222_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='popit.Organization', verbose_name='organization'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='popit.Person', verbose_name='person'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='popit.Post', verbose_name='post'),
        ),
    ]