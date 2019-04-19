# file not used anymore - used for create operation

import helper.py

def CreateDatabaseModel(dbName):
    dbId = helper.UniqueDB(dbName)
    if(dbId!=0):
        return dbId
    dbId = models.Database.objects.all().aggregate(Max('db_id'))['db_id__max']
    id(dbId==None):
        dbId = 0
    dbId += 1
    dbObj = models.Database(db_id=dbId, db_name=dbName)
    dbObj.save()
    return dbId

def GetNextRID(dbId):
    rId = models.DBTables.objects.all().aggregate(Max('r_id'))['r_id__max']
    if(rId==None):
        rId=0
    return rId+1
    
def GetIdOfNonTempRel(dbId):
    rel = models.DBTables.objects.filter(db_id=dbId, r_name="non_temporal")
    if(rel.exists()):
        return rel.first().r_id
    rID = GetNewRID(dbId)
    dbObj = helper.GetDBObject(dbId)
    dbtObj = models.DBTables(db_id=dbObj, r_id=rId, r_name="non_temporal")
    dbtObj.save()
    return rId
        

def InsertIntoNonTempRel(dbId, attr, aId):
    # rId = GetIdOfNonTempRel(dbId)
    rId, aId = helper.UniqueAttr(dbId, aName)
    if(aId==0):
        dbtaObj = models.DBTAttribute(r_id=rId, a_id=aId, a_name=attr[1], a_type=attr[2], isTemp=False)
        dbtaObj.save()
        return 1
    else
        return 0

def CreateDBTAttributeModel(dbId, relName):
    attrList = []
    rId = UniqueRelUsingDBId(dbId, relName)
    rel = helper.GetRelObject(rId)
    attrs = models.DBTAttribute.objects.filter(r_id=rel)
    if(relName=="non_temporal"):
        pass
    else:
        
        
def CreateDBTablesModel(dbId, relName):
    rId = GetNewRID(dbId)
    dbObj = helper.GetDBObject(dbId)
    dbtObj = models.DBTables(db_id=dbObj, r_id=rID, r_name=relName)
    dbtObj.save()
    CreateDBTAttributeModel(dbId, relName)
    return 1
    
def InsertIntoTempRel(dbId, attr):
    aName = "t_"+attr[1]
    rId = helper.UniqueRelUsingDBId(dbId, relName)
    if(rId!=0):
        return 0
    return CreateDBTablesModel(dbId, relName)
    
def CreateRels(dbId, attributes):
    aId = 1
    for attr in attributes:
        if(attr[0]==False):
            InsertIntoNonTempRel(dbId, attr, aId)
            aId += 1
        else:
            InsertIntoTempRel(dbId, attr)
                
def Main(dbName, attributes):
    dbId = CreateDatabaseModel(dbName)
    ret = CreateRels(dbId, attributes)
    
                