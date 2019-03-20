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
		attributes[str(i)]=str(data['attributes'][i])
	
	print(dbName)
	print(relName)
	print(attributes)
	
	helper.AddRel(dbName, relName, attributes)
	
	print("="*20)
	return HttpResponse(1);
	

@csrf_exempt
def GetRel(request):
	print("="*20)
	# print(request.POST)
	
	dbName = str(request.POST['dbName'])
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
	