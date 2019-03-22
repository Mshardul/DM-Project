from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'create/$', views.CreteRel, name="createRel"),
    url(r'get_rel/$', views.GetRel, name="getRel"),
    url(r'check_duplicate/$', views.CheckRel, name="checkDuplicateRel"),
    url(r'', views.Home, name="homepage"),
]