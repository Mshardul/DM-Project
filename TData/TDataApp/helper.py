import models
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

'''
    return type of every method is added as its first multi-line comment.
    parameters accepted, are clear from their name.
'''
    
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
    
def GetRels(dbName):
    ''' {0: db does not exists; list_of_rels_in_the_db: otherwise} '''
    print('getting all the relations in the db')
    dbId = UniqueDB(dbName)
    if(dbId==0):
        return 0
    rel = models.DBTables.objects.filter(db_id=dbId).all()
    rels=[]
    for r in rel:
        rels.append(r.r_name)
    return rels

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
    
def CreateDBTablesModel(dbName, relName):
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
    
def CreateDBTAttributeModel(dbName, relName, attributes):
    ''' {-1: rel duplication; 1: otherwise} '''
    dbId, rId = CreateDBTablesModel(dbName, relName)
    if(rId==0):
        return -1
    attrs_list=attributes.keys()
    i=1 #starts from 1, as we are not giving 'add column later' option
    relObj = GetRelObject(dbId, rId)
    for attr in attrs_list:
        dbtaObj = models.DBTAttribute(r_id=relObj, a_id=i, a_name=attr, a_type=int(attributes[attr]), is_temp=False)
        dbtaObj.save()
        i+=1
    return 1
    
def AddRel(dbName, relName, attributes):
    ''' {-1: rel duplication; 1: success, 0: exception}'''
    try:
        print('adding entries to all the db tables')
        return CreateDBTAttributeModel(dbName, relName, attributes)
    except:
        return 0