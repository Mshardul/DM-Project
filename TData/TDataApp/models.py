# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DataTypes(models.Model):
	dt_id = models.IntegerField(primary_key=True)
	dt_name = models.CharField(max_length=20, null=False)
	
class Database(models.Model):
	db_id = models.IntegerField(primary_key=True)
	db_name = models.CharField(max_length=20, null=False)

class DBTables(models.Model):
	class Meta(object):
		unique_together = (('db_id', 'r_id'), )
	db_id = models.ForeignKey(Database, on_delete=models.CASCADE)
	r_id = models.IntegerField(null=False)
	r_name = models.CharField(max_length=20, null=False)

class DBTAttribute(models.Model):
	class Meta(object):
		unique_together = (('db_id', 'r_id', 'a_id'))
	db_id = models.ForeignKey(Database, on_delete=models.CASCADE)
	r_id = models.ForeignKey(DBTables, on_delete=models.CASCADE)
	a_id = models.IntegerField(null=False)
	a_name = models.CharField(max_length=20, null=False)
	a_type = models.CharField(max_length=20, null=False)
	is_temp = models.BooleanField(null=False)

# dynamic tables to be created as well.
