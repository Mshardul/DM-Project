# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from . import helper

import json
import pprint

# Create your views here.

''' webpages '''
def Base(request):
	return render_to_response('base.html')
	
def Home(request):
	return render_to_response('home.html')

def Create(request):
	return render_to_response('create.html')
	
def Retrieve(request):
	return render_to_response('retrieve.html')
	
def Readme(request):
	return render_to_response('readme.html')
	
def Upload(request):
	return render_to_response('upload.html')
	
def Temporalize(request):
	return render_to_response('temporalize.html')

def Admin(request):
	return render_to_response('admin.html')

def Insert(request):
	return render_to_response('insert.html')

def Delete(request):
	return render_to_response('delete.html')
''' controllers '''

# --------------> temporalize

@csrf_exempt
def GetDBList(request):
	dbList = helper.GetDBFromFolder()
	print(dbList)
	return HttpResponse(json.dumps(dbList))

@csrf_exempt
def GetRelList(request):
	dbName = json.loads(request.POST.get('dbName'))
	print(dbName)
	if(dbName==None):
		return HttpResponse(0)
	relList = helper.GetRelFromDB(dbName)
	print(relList)
	return HttpResponse(json.dumps(relList))
	
@csrf_exempt
def GetAttrList(request):
	dbName = json.loads(request.POST.get('dbName'))
	relName = json.loads(request.POST.get('relName'))
	if(dbName==None or relName==None):
		return HttpResponse(0)
	attrList = helper.GetAttrFromRel(dbName, relName)
	return HttpResponse(json.dumps(attrList))
	
@csrf_exempt
def TempRel(request):
	data=json.loads(request.POST['data'])
	dbName = data['dbName']
	relName = data['relName']
	attrList = data['attributes']
	
	x = helper.MakeTemp(dbName, relName, attrList)
	
	return HttpResponse(x)
	
# --------------> admin

@csrf_exempt
def GetSql(request):
	sqlInfo = helper.GetSql()
	return HttpResponse(json.dumps(sqlInfo))
	
@csrf_exempt
def ExecQuery(request):
	data = json.loads(request.POST['data'])
	
	dbName = data['dbName']
	relName = data['relName']
	query = data['query']
	attr = (data['attr']).split(",")
	
	print("Query obtained: "+query)
	x = helper.ExecQuery(dbName, relName, query, attr)
	return HttpResponse(x)
	
@csrf_exempt
def DelQuery(request):
	data = json.loads(request.POST['data'])
	
	dbName = data['dbName']
	relName = data['relName']
	query = data['query']
	queryId = data['queryId']
	
	x = helper.DelQuery(dbName, relName, query)
	return HttpResponse(x)

# --------------> insert
@csrf_exempt
def InsertQuery(request):
	data = json.loads(request.POST['data'])
	
	dbName = data['dbName']
	relName = data['relName']
	attrVal = data['attrVal']
	
	print(data)
	x = helper.InsertQuery(dbName, relName, attrVal)
	return HttpResponse(x)
	
@csrf_exempt
def DeleteQuery(request):
	data = json.loads(request.POST['data'])
	
	dbName = data['dbName']
	relNames = data['relNames']
	additionalRel = data['additionalRel']
	where = data['where']
	
	x=helper.DeleteQuery(dbName, relNames, additionalRel, where)
	return HttpResponse(x)