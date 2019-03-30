import helper
import dbAccess

def Main(dbName, attributes):
    dbId = helper.CreateDatabaseModel(dbName) #create db if not exists; return dbId
    dbObj = helper.GetDBObject(dbId)
    nonTempRId = helper.GetIdOfNonTempRel(dbId) #create non-temp rel if not exists; return rId
    rObj = helper.GetRelObject(nonTempRId)
    if(helper.DuplicateAttr(dbObj, rObj, attributes)==1):
        return -1
    nonTempAttr = []
    tempAttr = []
    for attr in attributes:
        if(attr[0]==False):
            nonTempAttr.append(attr)
            print("got non temporal attr", attr[1])
            helper.AddAttrToNonTemp(rObj, attr)
        else:
            tempAttr.append(attr)
            print("got temporal attr", attr[1])
            helper.AddTempRel(dbObj, attr)
            
    dbAccess.CreateNonTempTable(dbName, nonTempAttr)
    # 
    for attr in nonTempAttr:
        dbAccess.CreateTempTable(dbName, attr)
    
    return 1
