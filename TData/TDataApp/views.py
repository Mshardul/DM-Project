# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from . import helper

import json
import pprint

# Create your views here.

def Base(request):
	return render_to_response('base.html')
	
def Home(request):
	return render_to_response('home.html')

def Create(request):
	return render_to_response('create.html')
	
def Retrieve(request):
	return render_to_response('retrieve.html')
	

# @csrf_protect
@csrf_exempt
def CreteRel(request):
	print("="*20)
	
	data=json.loads(request.POST['data'])
	# print(data)
	dbName = data['dbName']
	relName = data['relName']
	attributes = data['attributes']
	
	for attr in attributes: #[bool isTemp, string attrName, int attrType]
		attr[0] = True if int(attr[0])==1 else False
		attr[1] = str(attr[1])
		attr[2] = int(attr[2])
	
	print(dbName)
	print(relName)
	print(attributes)
	
	resp = helper.AddRel(dbName, relName, attributes)
	
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