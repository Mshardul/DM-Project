from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'create_rel/$', views.CreteRel, name="createRel"),
    url(r'get_rel/$', views.GetRel, name="getRel"),
    url(r'check_duplicate/$', views.CheckRel, name="checkDuplicateRel"),
    url(r'get_db/$', views.GetDB, name="GetDBs"),
    
    url(r'base/$', views.Base, name="base"),
    url(r'create/$', views.Create, name="createOperation"),
    url(r'retrieve/$', views.Retrieve, name="retrieveOperation"),
    url(r'', views.Home, name="homepage"),
]