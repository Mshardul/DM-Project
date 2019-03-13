# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse

# Create your views here.
def Home(request):
	# return HttpResponse("Hi!!!")
	return render_to_response('home.html')