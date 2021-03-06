# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-04-18 19:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Database',
            fields=[
                ('db_id', models.IntegerField(primary_key=True, serialize=False)),
                ('db_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DataTypes',
            fields=[
                ('dt_id', models.IntegerField(primary_key=True, serialize=False)),
                ('dt_name', models.CharField(max_length=20)),
                ('dt_sql', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='DBTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_id', models.IntegerField()),
                ('r_name', models.CharField(max_length=20)),
                ('db_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TDataApp.Database')),
            ],
        ),
        migrations.CreateModel(
            name='DBTAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_id', models.IntegerField()),
                ('a_name', models.CharField(max_length=20)),
                ('a_type', models.CharField(max_length=20)),
                ('is_temp', models.BooleanField()),
                ('is_notNull', models.BooleanField()),
                ('is_unique', models.BooleanField()),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TDataApp.DBTable')),
            ],
        ),
        migrations.CreateModel(
            name='DBTAttributeNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_id', models.IntegerField()),
                ('a_name', models.CharField(max_length=20)),
                ('a_type', models.CharField(max_length=10)),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TDataApp.DBTable')),
            ],
        ),
        migrations.CreateModel(
            name='SQL',
            fields=[
                ('sql_id', models.IntegerField(primary_key=True, serialize=False)),
                ('db_name', models.CharField(max_length=100)),
                ('rel_name', models.CharField(max_length=100)),
                ('sql', models.CharField(max_length=1000)),
                ('attr_list', models.CharField(max_length=100)),
            ],
        ),
    ]
