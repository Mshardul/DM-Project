import models
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
import createOp

def GetDBObject(dbId):
    ''' {db object} //useful for fk references '''
    print("getting db objects")
    obj = models.Database.objects.filter(db_id=dbId).first()
    return obj

def GetRelObject(dbId, relId):
    ''' {rel object} //useful for fk references '''
    print("getting rel objects")
    obj = models.DBTables.objects.filter(db_id=dbId, r_id=relId).first()
    return obj
    
def UniqueDB(dbName):
    ''' {0: db does not exist; db_id: otherwise} '''
    print('checking if db exists')
    db = models.Database.objects.filter(db_name=dbName)
    if db.exists():
        print("got db")
        return db.first().db_id
    print("no db")
    return 0

def UniqueRel(dbName, relName):
    ''' {(0, 0): db does not exist; (1, 0): rel does not exist; (db_id, rel_id): otherwise} '''
    print('checking if relation exists in the dbName given')
    dbId = UniqueDB(dbName)
    if dbId==0:
        print("DB does not exist")
        return (0, 0)
    rel = models.DBTables.objects.filter(db_id=dbId, r_name=relName)
    if rel.exists():
        print("rel exists")
        return (dbId, rel.first().r_id)
    print("rel does not exist")
    return (1, 0)

def UniqueRelUsingDBId(dbId, relName):
    ''' {0: rel does not exist; rel_id: otherwise} '''
    print('checking if relation exists in the dbId given')
    rel = models.DBTables.objects.filter(db_id=dbId, r_name=relName)
    if rel.exists():
        return (rel.first().r_id)
    return 0
    
# def UniqueAttr(dbId, aName): #checks for uniqueness of attribute name in "non temporal" table of database dbName
#     rId = UniqueRelUsingDBId(dbId, "non_temporal")
#     if(rId==0):
#         return (0, -1)
#     DBTAttribute
#     rel = GetRelObject(dbId, rId)
#     attr = models.DBTAttribute.objects.filter(r_id=rel, a_name=aName)
#     if(attr.exists()):
#         return (rId, attr.first().aId)
#     return (rId, 0)

def UniqueAttrInNonTempTable(dbId, attributes):
    rId = GetIdOfNonTempRel(dbId)
    attrs = 
    
    
def CreateDatabaseModel(dbName):
    ''' {db_id} //creates db, if does not exist '''
    print('creating db')
    dbId = UniqueDB(dbName)
    if(dbId!=0): #a db with the same name, already exists
        return dbId
    else:
        dbId = models.Database.objects.all().aggregate(Max('db_id'))['db_id__max']
    if(dbId==None):
        dbId=0
    dbId+=1
    dbObj = models.Database(db_id=dbId, db_name=dbName)
    dbObj.save()
    return dbId

def CreateDBTablesModel(dbName, relName, isTemp):
    ''' {(db_id, 0): if rel does not exist; (db_id, rel_id): otherwise} '''
    print('creating relation in given dbName')
    dbId = CreateDatabaseModel(dbName)
    if(UniqueRelUsingDBId(dbId, relName)!=0):
        return (dbId, 0)
    rId = models.DBTables.objects.all().aggregate(Max('r_id'))['r_id__max']
    if(rId==None):
        rId=0
    rId+=1
    dbObj = GetDBObject(dbId)
    dbtObj = models.DBTables(db_id=dbObj, r_id=rId, r_name=relName)
    dbtObj.save()
    return (dbId, rId)

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
        
def AddRel(dbName, attributes): 
    ''' {-1: rel duplication; 1: success, 0: exception}'''
    try:
        print('adding entries to all the db tables')
        return createDB.Main(dbName, attributes)
    except:
        return 0