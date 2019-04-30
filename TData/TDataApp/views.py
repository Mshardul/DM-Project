# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from . import helper

import json

# Create your views here.

''' webpages '''
def Base(request):
	return render_to_response('base.html')
	
def Home(request):
	return render_to_response('home.html')
	
def Abstract(request):
	return render_to_response('abstract.html')
	
def Developers(request):
	return render_to_response('developers.html')

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
	
def Update(request):
	return render_to_response('update.html')

def Delete(request):
	return render_to_response('delete.html')

def RetrieveTemp(request):
	return render_to_response('retrieveTemp.html')

def Query(request):
	return render_to_response('query.html')

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
	# additionalRel = data['additionalRel']
	where = data['where']
	additionalQuery = data['additionalQuery'].strip()
	
	x=helper.DeleteQuery(dbName, relNames, where, additionalQuery)
	return HttpResponse(x)
	
# --------------> update
@csrf_exempt
def UpdateQuery(request):
	data = json.loads(request.POST['data'])
	
	dbName = data['dbName']
	relName = data['relName']
	attrVal = data['attrVal']
	where = data['where'].strip()
	additionalQuery = data['additionalQuery'].strip()
	
	print(dbName, relName, attrVal, where, additionalQuery)
	
	if(len(relName)==0):
		return 1
	x = helper.UpdateQuery(dbName, relName, attrVal, where, additionalQuery)
	
	return HttpResponse(x)

# --------------> retrieve
@csrf_exempt
def GetTempAttrList(request):
	dbName = json.loads(request.POST.get('dbName'))
	relName = json.loads(request.POST.get('relName'))
	if(dbName==None or relName==None):
		return HttpResponse(0)
	attrList = helper.GetTempAttrFromRel(dbName, relName)
	return HttpResponse(json.dumps(attrList))
	
@csrf_exempt
def RetrieveTempQuery(request):
	data = json.loads(request.POST['data'])
	
	print(data)
	dbName = data['dbName']
	relName = data['relName']
	tempRelList = data['attributes']
	query = data['query']
	val = data['val']
	print(dbName, relName, tempRelList, query, val)
	x = helper.ExecRetrieveTemp(dbName, relName, tempRelList, query, val)
	return HttpResponse(json.dumps(x))