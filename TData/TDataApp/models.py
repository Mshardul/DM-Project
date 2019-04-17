# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

def get_file_path(instance, filename):
    return os.path.join('db_files', str(instance.id), filename)
	
# Create your models here.
class DataTypes(models.Model):
	dt_id = models.IntegerField(primary_key=True)
	dt_name = models.CharField(max_length=20, null=False)
	dt_sql = models.CharField(max_length=20, null=False)
	
class Database(models.Model):
	db_id = models.IntegerField(primary_key=True)
	db_name = models.CharField(max_length=20, null=False)
	# db_file = models.FileField(upload_to=get_file_path)

class DBTable(models.Model):
	# class Meta(object):
		# unique_together = (('db_id', 'r_id'), )
	db_id = models.ForeignKey(Database, on_delete=models.CASCADE)
	r_id = models.IntegerField(null=False)
	r_name = models.CharField(max_length=20, null=False)

class DBTAttribute(models.Model): #was being used for 'Create'; not anymore
	# class Meta(object):
		# unique_together = (('db_id', 'r_id', 'a_id'))
	# db_id = models.ForeignKey(Database, on_delete=models.CASCADE) #we can remove this, and make r_id as the only ForeignKey; by making r_id as AutoField in DBTable class
	r_id = models.ForeignKey(DBTable, on_delete=models.CASCADE)
	a_id = models.IntegerField(null=False)
	a_name = models.CharField(max_length=20, null=False)
	a_type = models.CharField(max_length=20, null=False) #foreign to DataTypes
	is_temp = models.BooleanField(null=False) #has no significance now
	is_notNull = models.BooleanField(null=False)
	is_unique = models.BooleanField(null=False)
    
class DBTAttributeNew(models.Model):
    r_id = models.ForeignKey(DBTable, on_delete=models.CASCADE)
    a_id = models.IntegerField(null=False)
    a_name = models.CharField(max_length=20, null=False)
    a_type = models.CharField(max_length=10, null=False)

class SQL(models.Model):
    sql_id = models.IntegerField(primary_key=True)
    db_name = models.CharField(max_length=100, null=False)
    rel_name = models.CharField(max_length=100, null=False)
    sql = models.CharField(max_length=1000, null=False)
    
# dynamic tables to be created as well.
