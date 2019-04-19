from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

import os
import json
import datetime

from . import models
from . import dbAccess

# working with external db //already present with end user

def UniqueDB(dbName):
    ''' {0: db does not exist; db_id: otherwise} '''
    print('checking if db exists')
    db = models.Database.objects.filter(db_name=dbName)
    if db.exists():
        print("got db")
        return db.first().db_id
    print("no db")
    return 0
    
def UniqueRel(dbId, relName):
    ''' {0: rel does not exist; rel_id: otherwise} '''
    print('checking if relation exists in the dbId given')
    rel = models.DBTable.objects.filter(db_id=dbId, r_name=relName)
    if rel.exists():
        return (rel.first().r_id)
    return 0

def GetDBObject(dbId):
    ''' {db object} //useful for fk references '''
    print("getting db objects")
    obj = models.Database.objects.filter(db_id=dbId).first()
    return obj

def GetRelObject(rId):
    ''' {rel object} //useful for fk references '''
    print("getting rel objects")
    obj = models.DBTable.objects.filter(r_id=rId).first()
    return obj
    
def GetDBFolder():
    baseDir = settings.BASE_DIR
    dbFolder = os.path.join(baseDir, 'TDataApp/db_files')
    return dbFolder
    
def CreateAttrModel(rObj, attrName, attrType):
    print("creating attr models")
    # not checking for uniqueness as of now
    aId = models.DBTAttributeNew.objects.all().aggregate(Max('a_id'))['a_id__max']
    if(aId==None):
        aId=0
    aId+=1
    aObj = models.DBTAttributeNew(r_id=rObj, a_id=aId, a_name=attrName, a_type=attrType)
    aObj.save()
    return 1

def CreateRelModel(dbId, dbObj, relName):
    print("creating rel model")
    rId = UniqueRel(dbId, relName)
    if(rId!=0):
        return -1
    rId = models.DBTable.objects.all().aggregate(Max('r_id'))['r_id__max']
    if(rId==None):
        rId=0
    rId += 1
    rObj = models.DBTable(db_id=dbObj, r_id=rId, r_name=relName)
    rObj.save()
    print('created rel model')
    return rId
    
def CreateDatabaseModel(dbName):
    print("creating db model")
    dbId = UniqueDB(dbName)
    if(dbId!=0):
        return dbId
    dbId = models.Database.objects.all().aggregate(Max('db_id'))['db_id__max']
    if(dbId==None):
        dbId=0
    dbId+=1
    dbObj = models.Database(db_id=dbId, db_name=dbName)
    dbObj.save()
    print("created db model")
    return dbId
# usage known

def GetDBFromFolder(): # views.GetDBList()
    print("=="*10)
    dbFolder = GetDBFolder()
    print(dbFolder)
    dbList = []
    for item in enumerate(os.listdir(dbFolder)):
        extension = (item[1].split("."))[-1]
        extensionL = -1-len(extension)
        if(extension=="db"):
            dbList.append(item[1])
            # dbList.append(item[1][:extensionL])
    print("=="*10)
    return dbList
    
def GetRelFromDB(dbName): # views.GetRelList()
    dbFolder = GetDBFolder()
    relList = dbAccess.GetRelFromDB(dbFolder, dbName)
    return relList
    
def GetAttrFromRel(dbName, relName): # views.GetAttrList()
    dbFolder = GetDBFolder()
    attrList = dbAccess.GetAttrFromRel(dbFolder, dbName, relName)
    return attrList
    
def AttrAlreadyTemp(dbName, tableName): # MakeTemp()
    dbFolder = GetDBFolder()
    return dbAccess.AttrAlreadyTemp(dbFolder, dbName, tableName)
    
def AddSQL(dbName, relName, sql, attrList): # MakeTemp()
    sqlObj = models.SQL.objects.filter(db_name=dbName, rel_name=relName)
    if(sqlObj.exists()):
        return -1
    sqlId = models.SQL.objects.all().aggregate(Max('sql_id'))['sql_id__max']
    if(sqlId==None):
        sqlId=0
    sqlId+=1
    attrs = ",".join(attrList)
    sqlObj = models.SQL(sql_id=sqlId, db_name=dbName, rel_name=relName, sql=sql, attr_list=attrs)
    sqlObj.save()
    return 1

def CreateModels(dbName, relName, tempAttrName, tempAttrType): # views.TempRel()
    dbId = CreateDatabaseModel(dbName)
    dbObj = GetDBObject(dbId)
    rId = CreateRelModel(dbId, dbObj, relName)
    rObj = GetRelObject(rId)
    if(rId==-1):
        return rId
    for i in range(len(tempAttrName)):
        CreateAttrModel(rObj, tempAttrName[i], tempAttrType[i])
    return 1
    
def GetSql(): # views.GetSql()
    sqlObj = models.SQL.objects.all()
    ret = []
    for sql in sqlObj:
        temp = []
        temp.append(sql.sql_id)
        temp.append(sql.db_name)
        temp.append(sql.rel_name)
        temp.append(sql.sql)
        temp.append(sql.attr_list)
        ret.append(temp)
    print(ret)
    return ret

def ExecQuery(dbName, relName, query, attr): # views.ExecQuery()
    dbFolder = GetDBFolder()
    x = dbAccess.ExecuteQuery(dbFolder, dbName, query)
    
    if x==1:
        y = dbAccess.GetTempData(dbFolder, dbName, relName, attr)
        if(y==1):
            return DelQuery(dbName, relName, query)
    return x
    
def DelQuery(dbName, relName, query): # views.DelQuery()
    sqlObj = models.SQL.objects.filter(db_name=dbName, rel_name=relName, sql=query)
    try:
        if(sqlObj.exists()):
            sqlObj.delete()
    except Error as e:
        return -1
    return 1

def MakeTemp(dbName, relName, attrList): # views.TempRel()
    dbFolder = GetDBFolder()
    pk, pkType = dbAccess.GetPK(dbFolder, dbName, relName)
    
    # to store in sql model
    sql = ""
    
    # to create other models
    tempAttrName = []
    tempAttrType = []
    
    x = 0
    print("*"*10)
    for attr in attrList:
        print attr
        if(attr[0]==1):
            attrName = str(attr[1])
            attrType = str(attr[2])
            
            tempAttrName.append(attrName)
            tempAttrType.append(attrType)
            
            tableName = "hist_"+((dbName).split("."))[0]+"_"+relName+"_"+attrName
            if(AttrAlreadyTemp(dbName, tableName)):
                continue
            rel1 = "sd_"+attrName
            rel2 = "ed_"+attrName
            sql += "CREATE TABLE '"+tableName+"' ('"+pk+"' "+pkType+", '"+rel1+"' TEXT, '"+attrName+"' "+attrType+", '"+rel2+"' TEXT); "
            # CREATE TABLE <tableName> (<pk> <pkType>, sd_<attrName> TEXT, <attrName> <attrType>, ed_<attrName> TEXT); 
    
    if(sql!=""):
        x = AddSQL(dbName, relName, sql, tempAttrName)
        CreateModels(dbName, relName, tempAttrName, tempAttrType) # not significant, as of now
    
    return x