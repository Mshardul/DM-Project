import models
import datetime
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os
import json
import dbAccess

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
    
def GetRelId(dbId, relName):
    rel = models.DBTable.objects.filter(db_id=dbId, r_name=relName)
    if(rel.exists()):
        return rel.first().r_id
    else:
        return 0

def GetNextRId():
    rId = models.DBTable.objects.all().aggregate(Max('r_id'))['r_id__max']
    if(rId==None):
        rId=0
    rId+=1
    return rId
    
def GetIdOfNonTempRel(dbId):
    print("getting id of non temporal row")
    rId = GetRelId(dbId, "non_temporal")
    if(rId==0):
        rId = GetNextRId()
        CreateNonTempRel(dbId, rId)
    return rId

def CreateNonTempRel(dbId, rId):
    print("creating non temporal row")
    dbObj = GetDBObject(dbId)
    rObj = models.DBTable(db_id=dbObj, r_id=rId, r_name="non_temporal")
    rObj.save()
    
def DuplicateNonTempAttr(dbObj, rObj, aName):
    attr = models.DBTAttribute.objects.filter(r_id=rObj, a_name=aName)
    if(attr.exists()):
        return 1
    return 0
    
def DuplicateTempRel(dbObj, rName):
    rel = models.DBTable.objects.filter(db_id=dbObj, r_name=rName)
    if(rel.exists()):
        return 1
    return 0
    
def DuplicateAttr(dbObj, rObj, attributes):
    print("checking for duplicacy")
    for attr in attributes:
        if(attr[0]==False):
            if(DuplicateNonTempAttr(dbObj, rObj, attr[1])==1):
                print("duplicacy found with ", attr[1])
                return 1
        else:
            if(DuplicateTempRel(dbObj, attr[1])==1):
                print("duplicacy found with ", attr[1])
                return 1
    print("no duplicacy found")
    return 0

def GetNextAId():
    aId = models.DBTAttribute.objects.all().aggregate(Max('a_id'))['a_id__max']
    if(aId==None):
        aId=0
    aId+=1
    return aId
    
def AddAttrToNonTemp(rObj, attr):
    print("Adding non temp attribute ", attr[1])
    aId = GetNextAId()
    dbtaObj = models.DBTAttribute(r_id=rObj, a_id=aId, a_name=attr[1], a_type=attr[2], is_temp=attr[0], is_notNull=attr[3], is_unique=attr[4])
    dbtaObj.save()
    return 1
    
def AddAttrToTemp(rObj, aName, aType):
    print("Adding attributes to temporal rel")
    aId = GetNextAId()
    dbtaObj = models.DBTAttribute(r_id=rObj, a_id=aId, a_name=aName, a_type=aType, is_temp=True, is_notNull=True, is_unique=False)
    dbtaObj.save()
    return 1
    
def AddTempRel(dbObj, attr):
    print("Adding temporal relation ", attr[1])
    rId = GetNextRId()
    dbtObj = models.DBTable(db_id=dbObj, r_id=rId, r_name=attr[1])
    dbtObj.save()
    rObj = GetRelObject(rId)
    AddAttrToTemp(rObj, attr[1], attr[2])

# working with external db //already present with end user

def GetDBFolder():
    baseDir = settings.BASE_DIR
    dbFolder = os.path.join(baseDir, 'TDataApp/db_files')
    return dbFolder
    
def GetDBFromFolder():
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
    
def GetRelFromDB(dbName):
    dbFolder = GetDBFolder()
    relList = dbAccess.GetRelFromDB(dbFolder, dbName)
    return relList
    
def GetAttrFromRel(dbName, relName):
    dbFolder = GetDBFolder()
    attrList = dbAccess.GetAttrFromRel(dbFolder, dbName, relName)
    return attrList

def AddSQL(dbName, relName, sql):
    sqlObj = models.SQL.objects.filter(db_name=dbName, rel_name=relName)
    if(sqlObj.exists()):
        return -1
    sqlId = models.SQL.objects.all().aggregate(Max('sql_id'))['sql_id__max']
    if(sqlId==None):
        sqlId=0
    sqlId+=1
    sqlObj = models.SQL(sql_id=sqlId, db_name=dbName, rel_name=relName, sql=sql)
    sqlObj.save()
    return 1
    
def GetSql():
    sqlObj = models.SQL.objects.all()
    ret = []
    for sql in sqlObj:
        temp = []
        temp.append(sql.sql_id)
        temp.append(sql.db_name)
        temp.append(sql.rel_name)
        temp.append(sql.sql)
        ret.append(temp)
    return ret

def ExecQuery(dbName, relName, query):
    dbFolder = GetDBFolder()
    x = dbAccess.ExecuteQuery(dbFolder, dbName, query)
    if x==1:
        y = DelQuery(dbName, relName, query)
        return y
    return x
    
def DelQuery(dbName, relName, query):
    sqlObj = models.SQL.objects.filter(db_name=dbName, rel_name=relName, sql=query)
    try:
        if(sqlObj.exists()):
            sqlObj.delete()
    except Error as e:
        return -1
    return 1


def CreateModels(dbName, relName, tempAttrName, tempAttrType):
    dbId = CreateDatabaseModel(dbName)
    dbObj = GetDBObject(dbId)
    rId = CreateRelModel(dbId, dbObj, relName)
    rObj = GetRelObject(rId)
    if(rId==-1):
        return rId
    for i in range(len(tempAttrName)):
        CreateAttrModel(rObj, tempAttrName[i], tempAttrType[i])
    return 1
    
def AttrAlreadyTemp(dbName, tableName):
    dbFolder = GetDBFolder()
    return dbAccess.AttrAlreadyTemp(dbFolder, dbName, tableName)
    