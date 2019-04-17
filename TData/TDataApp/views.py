# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from . import helper
import createOp

import json
import pprint

import datetime

# Create your views here.

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
	
# @csrf_protect
@csrf_exempt
def CreateRel(request):
	print("="*20)
	
	data=json.loads(request.POST['data'])
	print(data)
	dbName = data['dbName']
	relName = data['relName']
	attributes = data['attributes']
	
	for attr in attributes: #[bool isTemp, string attrName,]
		attr[0] = True if int(attr[0])==1 else False
		attr[1] = str(attr[1])
		# attr[2] = int(attr[2])
		# attr[3] = True if int(attr[3])==1 else False
		# attr[4] = True if int(attr[4])==1 else False
	
	print(dbName)
	# print(relName)
	print(attributes)
	
	resp = createOp.Main(dbName, attributes) #relName #not required as of now
	
	print("="*20)
	return HttpResponse(resp);
	

@csrf_exempt
def GetRel(request):
	print("="*20)
	
	dbName = json.loads(request.POST['dbName'])
	print dbName
	rels = helper.GetRels(dbName)
	print rels
	print("="*20)
	if rels==0:
		print("sending empty string")
		return HttpResponse("")
	else:
		print("sending list of relations")
		return HttpResponse(rels)

@csrf_exempt
def CheckRel(request):
	dbName = json.loads(request.POST['dbName'])
	relName = json.loads(request.POST['relName'])
	db_id, rel_id = helper.UniqueRel(dbName, relName)
	if(db_id==0):
		return HttpResponse("-1")
	elif(rel_id==0):
		return HttpResponse("1")
	else:
		return HttpResponse("0")
	
def DisplayAllDB(request):
	pass

@csrf_exempt
def GetDB(request):
	dbList = helper.GetAllDB()
	print(dbList)
	return HttpResponse(dbList)
	
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
	print("="*20)
	print(dbName, relName)
	print("="*20)
	
	if(dbName==None or relName==None):
		return HttpResponse(0)
	attrList = helper.GetAttrFromRel(dbName, relName)
	print(attrList)
	return HttpResponse(json.dumps(attrList))
	
@csrf_exempt
def TempRel(request):
	data=json.loads(request.POST['data'])
	dbName = data['dbName']
	relName = data['relName']
	attrList = data['attributes']
	
	print(attrList)
	
	sql = ""
	
	now = datetime.datetime.now()
	today = now.strftime("%Y-%m-%d")
	
	tempAttrName = []
	tempAttrType = []
	print("*"*10)
	for attr in attrList:
		print attr
		if(attr[0]==1):
			attrName = str(attr[1])
			attrType = str(attr[2])
			
			tempAttrName.append(attrName)
			tempAttrType.append(attrType)
			
			tableName = "hist_"+((dbName).split("."))[0]+"_"+attrName
			if(helper.AttrAlreadyTemp(dbName, tableName)):
				continue
			rel1 = "sd_"+attrName
			rel2 = "ed_"+attrName
			
			sql += "CREATE TABLE "+tableName+" ("+rel1+" TEXT, "+attrName+" "+attrType+", "+rel2+" TEXT)"
	
	x = helper.AddSQL(dbName, relName, sql)
	
	helper.CreateModels(dbName, relName, tempAttrName, tempAttrType)
	return HttpResponse(x)
	
	
	# CREATE TABLE <TABLE_NAME> ( <REL1> "TEXT", <ATTRNAME> <ATTRTYPE>, <REL2> "TEXT")
	
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
	
	x = helper.ExecQuery(dbName, relName, query)
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