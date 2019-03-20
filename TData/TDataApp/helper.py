from . import models

def UniqueDB(dbName): #given db name; return db_id, else 0
    db = models.Database.objects.filter(db_name=dbName)
    if db.exists():
        return db.first().db_id
    return 0

def UniqueRel(dbName, relName): #given rel name; returns rel_id, else 0
    dbId = UniqueDB(dbName)
    if dbId==0:
        return 0
    rel = models.DBTables.objects.filter(db_id=dbId, r_name=relName)
    if rel.exists():
        return rel.first().rel_id
    return 0
    
def GetRels(dbName): #given db name; get all its relations
    dbId = UniqueDB(dbName)
    if(dbId==0):
        return 0
    rel = models.DBTables.objects.filter(db_id=dbId).all()
    rels=[]
    for r in rel:
        rels.append(r.r_name)
    return rels
    
def AddRel(dbName, relName, attributes):
    db_id = UniqueDB(dbName)
    if db_id==0:
        pass #create new db
    #create new relation
    #create new attributes 

