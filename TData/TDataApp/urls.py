from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [    
    
    #retrieve
    url(r'get_tempAttrList/$', views.GetTempAttrList, name="GetTempAttrList"),
    url(r'ret_temp/$', views.RetrieveTempQuery, name="RetrieveTempQuery"),
    
    #delete
    url(r'deleteQuery/$', views.DeleteQuery, name="DeleteQuery"),
    
    #insert
    url(r'insertQuery/$', views.InsertQuery, name="InsertQuery"),
    
    #temporalize
    url(r'get_dbList/$', views.GetDBList, name="GetDBList"),
    url(r'get_relList/$', views.GetRelList, name="GetRelList"),
    url(r'get_attrList/$', views.GetAttrList, name="GetAttrList"),
    url(r'temp_rel/$', views.TempRel, name="TemporalizeQuery"),
    
    #update
    url(r'updateQuery/$', views.UpdateQuery, name="UpdateQuery"),
    
    #admin
    url(r'get_sql/$', views.GetSql, name="GetSql"),
    url(r'exec_query/$', views.ExecQuery, name="ExecuteQuery"),
    url(r'del_query/$', views.DelQuery, name="DeleteQuery"),
    
    #django-admin
    url(r'admin/$', views.Admin, name="Admin"),
    
    #html pages
    url(r'base/$', views.Base, name="base"),
    url(r'abstract/$', views.Abstract, name="Abstract"),
    url(r'developers/$', views.Developers, name="Developers"),
    url(r'upload/$', views.Upload, name="UploadOperation"),
    url(r'create/$', views.Create, name="CreateOperation"),
    url(r'makeTemp/$', views.Temporalize, name="Temporalize"),
    url(r'retrieveTemp/$', views.RetrieveTemp, name="RetrieveTempOperation"),
    url(r'insert/$', views.Insert, name="InsertOperation"),
    url(r'readme/$', views.Readme, name="Readme"),
    url(r'update/$', views.Update, name="UpdateOperation"),
    url(r'delete/$', views.Delete, name="DeleteOperation"),
    url(r'query/$', views.Query, name="QueryOperation"),
    url(r'', views.Home, name="homepage"),
    
    #not using anymore
    # url(r'create_rel/$', views.CreateRel, name="createRel"),
    # url(r'get_rel/$', views.GetRel, name="getRel"),
    # url(r'check_duplicate/$', views.CheckRel, name="checkDuplicateRel"), #not required as of now
    # url(r'get_db/$', views.GetDB, name="GetDBs"),
    # url(r'upload_file/$', views.UploadFile, name="uploadFile"),
]
