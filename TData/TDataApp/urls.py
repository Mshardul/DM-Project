from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'create_rel/$', views.CreateRel, name="createRel"),
    url(r'get_rel/$', views.GetRel, name="getRel"),
    # url(r'check_duplicate/$', views.CheckRel, name="checkDuplicateRel"), #not required as of now
    url(r'get_db/$', views.GetDB, name="GetDBs"),
    
    url(r'base/$', views.Base, name="base"),
    url(r'create/$', views.Create, name="createOperation"),
    url(r'upload/$', views.Upload, name="uploadOperation"),
    # url(r'upload_file/$', views.UploadFile, name="uploadFile"),
    url(r'retrieve/$', views.Retrieve, name="retrieveOperation"),
    url(r'readme/$', views.Readme, name="Readme"),
    url(r'makeTemp/$', views.Temporalize, name="Temporalize"),
    url(r'get_dbList/$', views.GetDBList, name="GetDBList"),
    url(r'get_relList/$', views.GetRelList, name="GetRelList"),
    url(r'get_attrList/$', views.GetAttrList, name="GetAttrList"),
    url(r'temp_rel/$', views.TempRel, name="TempRel"),
    
    url(r'admin/$', views.Admin, name="Admin"),
    
    url(r'get_sql/$', views.GetSql, name="GetSql"),
    url(r'exec_query/$', views.ExecQuery, name="ExecuteQuery"),
    url(r'del_query/$', views.DelQuery, name="DeleteQuery"),
    
    
    url(r'', views.Home, name="homepage"),
]