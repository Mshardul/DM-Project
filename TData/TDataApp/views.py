# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from . import helper

import json
import pprint
# Create your views here.
def Home(request):
	# return HttpResponse("Hi!!!")
	return render_to_response('home.html')
	
# @csrf_protect
@csrf_exempt
def CreteRel(request):
	print("="*20)
	
	data=json.loads(request.POST['data'])
	# print(data)
	dbName = data['dbName']
	relName = data['relName']
	attributes={}
	for i in data['attributes']:
		attributes[str(i)]=str(data['attributes'][i]) #{'attr1': 'type1'}
	
	print(dbName)
	print(relName)
	print(attributes)
	
	resp = helper.AddRel(dbName, relName, attributes)
	
	print("="*20)
	return HttpResponse(resp);
	

@csrf_exempt
def GetRel(request):
	print("="*20)
	# print(request.POST)
	
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
	