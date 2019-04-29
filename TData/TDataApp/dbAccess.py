from django.conf import settings
import sqlite3
from sqlite3 import Error
from sqlite3 import connect
    
import datetime

# working with external db //already present with end user

def CreateConnToExternalDB(dbFolder, dbName):
    dbPath = dbFolder+"/"+dbName
    conn = connect(dbPath)
    return conn
    
def GetRelFromDB(dbFolder, dbName): # helper.GetRelFromDB()
    curs = (CreateConnToExternalDB(dbFolder, dbName)).cursor()
    curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = []
    for tableName in curs.fetchall():
        tables.append(tableName[0])
    return tables

def GetAttrFromRel(dbFolder, dbName, relName): # helper.GetAttrFromRel()
    attrList = []
    curs = (CreateConnToExternalDB(dbFolder, dbName)).cursor()
    result = curs.execute("PRAGMA table_info('%s')" % relName).fetchall()
    column_names = list(zip(*result))[1] #implicit type of 'zip' not list in python 3.6
    column_types = list(zip(*result))[2]
    for i in range(len(column_names)):
        col = column_names[i]
        if(not(col[:3]=="ed_" or col[:3]=="sd_")):
            attrList.append([column_names[i], column_types[i]])
    # print(attrList)
    # pk, pkType = GetPK(dbFolder, dbName, relName) #use it, if we do not want to give user an option to temporalize pk.
    return attrList

def GetPK(dbFolder, dbName, relName): # helper.MakeTemp()
    curs = (CreateConnToExternalDB(dbFolder, dbName)).cursor()
    result = curs.execute("PRAGMA table_info('%s')" % relName).fetchall()
    for r in result:
        if(r[5]==1):
            print(r[1])
            return (r[1], r[2])
    
def ExecuteQuery(dbFolder, dbName, query): # helper.ExecQuery()
    curs = (CreateConnToExternalDB(dbFolder, dbName)).cursor()
    statement = query.split(";")
    try:
        print("printing all statements")
        for stmt in statement:
            print(stmt)
            curs.execute(stmt)
    except Error as e:
        print(e)
        return 0
    return 1

def AttrAlreadyTemp(dbFolder, dbName, tableName): # helper.AttrAlreadyTemp()
    curs = (CreateConnToExternalDB(dbFolder, dbName)).cursor()
    tables = GetRelFromDB(dbFolder, dbName)
    print(tables)
    if(tableName in tables):
        return True
    return False
    
def GetTempData(dbFolder, dbName, relName, attrs): # helper.ExecQuery()
    print("*"*20)
    conn = CreateConnToExternalDB(dbFolder, dbName)
    curs = conn.cursor()
    pk, pkType = GetPK(dbFolder, dbName, relName)

    dateNow = datetime.datetime.now()
    today = dateNow.strftime("%Y-%m-%d")
    
    sql = ""
    for attr in attrs:
        print("printing pk, attr values")
        if(pk==attr or attr==""):
            continue
        sql = "SELECT "+pk+", "+attr+" FROM "+relName+";"
        print(sql)
        valList = (curs.execute(sql)).fetchall()
        tableName = "hist_"+((dbName).split("."))[0]+"_"+relName+"_"+attr
        
        sql_insert = "INSERT INTO "+tableName+" ("+pk+", "+"sd_"+attr+", "+attr+") VALUES(?, ?, ?);"
        val = []
        for (p, a) in valList:
            val.append((p, today, a))
        print(val)
        curs.executemany(sql_insert, val)
        try:
            conn.commit()
        except Error as e:
            print(e)
            conn.rollback()
            return 0
    return 1

def InsertQuery(dbFolder, dbFullName, relName, attrVal): #helper.InsertQuery()
    dateNow = datetime.datetime.now()
    today = dateNow.strftime("%Y-%m-%d")
    
    dbName = (dbFullName.split("."))[0]
    
    pk = GetPK(dbFolder, dbFullName, relName)
    pkVal = 0
    tempAttr = []
    attrStr = ""
    valStr = ""
    
    print(attrVal)
    for attr in attrVal:
        attrStr += attr[0]+", "
        if(attr[1].upper()=="TEXT"):
            attr[2] = "'"+attr[2]+"'"
        valStr += attr[2]+", "
        attrTableName = "hist_"+dbName+"_"+relName+"_"+attr[0]
        if(AttrAlreadyTemp(dbFolder, dbFullName, attrTableName)):
            tempAttr.append(attr)
        if(attr[0]==pk[0]):
            pkVal = attr[2]
    
    if(pk[1].upper()=="TEXT"):
        pkVal = "'"+pkVal+"'"
        
    print(tempAttr)
    print(today, pk, pkVal)
    sql = "INSERT INTO "+relName+" ("+attrStr[:-2]+") VALUES ("+valStr[:-2]+"); "
    
    for attr in tempAttr:
        tempRelName = "hist_"+dbName+"_"+relName+"_"+attr[0]
        sql += "UPDATE "+tempRelName+" SET ed_"+attr[0]+" = '"+today+"' WHERE "+pk[0]+" = "+pkVal+" AND ed_"+attr[0]+" IS NULL;"
        sql += "INSERT INTO "+tempRelName+" ("+pk[0]+", sd_"+attr[0]+", "+attr[0]+") VALUES ("+pkVal+", '"+today+"', "+attr[2]+"); "
    
    print(sql)
    
    try:
        conn = CreateConnToExternalDB(dbFolder, dbFullName)
        curs = conn.cursor()
        for query in sql.split(";"):
            curs.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        conn.rollback()
        print(e)
        return 0
    return 1
    
def GetTempRel(dbFolder, dbFullName, relName):
    ret = []
    relList = GetRelFromDB(dbFolder, dbFullName)
    dbName = dbFullName.split(".")[0]
    str = "hist_"+dbName+"_"+relName
    n = len(str)
    for rel in relList:
        if(rel[:n]==str):
            ret.append(rel)
    return ret
    
'''
def DeleteQuery(dbFolder, dbName, relNames, where, additionalQuery): #helper.DeleteQuery()
    deleteRels =  ",".join(relNames)
    fromRels = ""
    # if(len(additionalRel)==0):
    #     fromRels = deleteRels
    # else:
    #     fromRels = deleteRels +","+ ",".join(additionalRel)
        
    sql = "DELETE FROM "+deleteRels
    if(where!=""):
        sql += " WHERE "+where
    if(additionalQuery!=""):
        sql += additionalQuery
    sql+=";"
    print(sql)
        
    try:
        conn = CreateConnToExternalDB(dbFolder, dbName)
        curs = conn.cursor()
        curs.execute(sql)
        conn.commit()
        conn.close()
    except Error as e:
        conn.rollback()
        print(e)
        return 0
    return 1
'''

'''
def DeleteQuery(dbFolder, dbFullName, relNames, where, additionalQuery): #helper.DeleteQuery()
    deleteRels =  ",".join(relNames)
    fromRels = ""
    # if(len(additionalRel)==0):
    #     fromRels = deleteRels
    # else:
    #     fromRels = deleteRels +","+ ",".join(additionalRel)
    
    sql_insert = ""
    for rel in relNames:
        pk = GetPK(dbFolder, dbFullName, rel)
        pkVal = []
        sql_insert = "SELECT "+pk+" FROM "+rel
        if(where!=""):
            sql_insert += " WHERE "+where
        if(additionalQuery!=""):
            sql_insert += additionalQuery
        sql_insert += ";"
        tempRel = GetTempRel(dbFolder, dbFullName, rel)
        for r in tempRel:
            attr = r.split("_")[-1]
            sql_insert += "UPDATE "+r+" SET ed_"+attr+" = '"+today+"' WHERE "+pk+" = "+pkVal+"; "
        
        

    sql_delete = "DELETE FROM "+deleteRels
    if(where!=""):
        sql_delete += " WHERE "+where
    if(additionalQuery!=""):
        sql_delete += additionalQuery
    sql_delete += ";"
    
    print(sql_insert)
    print(sql_delete)
        
    try:
        conn = CreateConnToExternalDB(dbFolder, dbFullName)
        curs = conn.cursor()
        
        curs.execute(sql_insert)
        pkVal = curs.fetchall()
        print(pkVal)
        
        # curs.execute(sql)
        # print(curs.fetchmany())
        # conn.commit()
        conn.close()
    except Error as e:
        conn.rollback()
        print(e)
        return 0
    return 1
'''

def DeleteQuery(dbFolder, dbFullName, relNames, where, additionalQuery): #helper.DeleteQuery()
    dateNow = datetime.datetime.now()
    today = dateNow.strftime("%Y-%m-%d")
    
    pk = []
    pkVal = []
    pkColType = []
    
    dbName = dbFullName.split(".")[0]
    for rel in relNames:
        pkCol = GetPK(dbFolder, dbFullName, rel)
        pk.append(rel+"."+pkCol[0])
        pkColType.append(pkCol[1])
        
    pkColList = ", ".join(pkColType)
    sql_select = "SELECT "
    pkList = ", ".join(pk)
    sql_select += pkList
    sql_select += " FROM "
    relList = ", ".join(relNames)
    sql_select += relList
    if(where!=""):
        sql_select += " WHERE "+where
    sql_select += ";"
    
    print(sql_select)
    
    tempRels = GetTempRel(dbFolder, dbFullName, relList)
    try:
        conn = CreateConnToExternalDB(dbFolder, dbFullName)
        curs = conn.cursor()
        curs.execute(sql_select)
        
        for val in curs.fetchall():
            pkVal.append(val[0])
        
        print(pkVal)
    except Exception as e:
        return 0
        
    sql_update = ""
    for rel in tempRels:
        attrName = rel.split("_")[-1]
        for val in pkVal:
            sql_update += "UPDATE "+rel
            sql_update += " SET ed_"+attrName
            sql_update += " = '"+today+"'"
            sql_update += " WHERE "+((pkList.split("."))[-1])+" = "
            if(pkColList.upper()=="TEXT"):
                sql_update += "'"+val+"'"
            else:
                sql_update += str(val)
            sql_update += " AND ed_"+attrName+" IS NULL;"
    
    print(sql_update)
    
    deleteRels =  ",".join(relNames)
    sql_delete = "DELETE FROM "+deleteRels
    if(where!=""):
        sql_delete += " WHERE "+where
    if(additionalQuery!=""):
        sql_delete += additionalQuery
    sql_delete+=";"
    print(sql_delete)
    
    try:
        conn = CreateConnToExternalDB(dbFolder, dbFullName)
        curs = conn.cursor()
        curs.execute(sql_delete)
        for query in sql_update.split(";"):
            curs.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        conn.rollback()
        print(e)
        return 0
    return 1
    
def UpdateQuery(dbFolder, dbFullName, relName, attrVal, where, additionalQuery): #helper.UpdateQuery
    print("*"*50)
    dateNow = datetime.datetime.now()
    today = dateNow.strftime("%Y-%m-%d")
    
    colName = []
    colType = []
    colVal = []
    
    print(dbFolder, dbFullName, relName, attrVal, where, additionalQuery)
    
    pk = GetPK(dbFolder, dbFullName, relName)
    pkName = pk[0]
    pkType = pk[1]
    
    sql = ""
    
    valStrList = []
    tempAttr = []
    
    dbName = (dbFullName.split("."))[0]
    n = len(attrVal)
    
    pkVal = [] 
    if(where!=""):
        sql_select = "SELECT "+pk[0]+" FROM "+relName+" WHERE "+where+";"
        try:
            conn = CreateConnToExternalDB(dbFolder, dbFullName)
            curs = conn.cursor()
            curs.execute(sql_select)
        
            for val in curs.fetchall():
                pkVal.append(val[0])
            
            print(pkVal)
        except Exception as e:
            print(e)
            return 0
    
    
    for attr in attrVal:
        if(attr[1].upper()=="TEXT"):
            attr[2] = "'"+attr[2]+"'"
        valStrList.append(attr[0]+"="+attr[2])
        
        attrTableName = "hist_"+dbName+"_"+relName+"_"+attr[0]
        if(AttrAlreadyTemp(dbFolder, dbFullName, attrTableName)):
            tempAttr.append(attr)
    
    if(pkType.upper()=="TEXT"):
        for val in pkVal:
            val = "'"+val+"'"
    print(pkVal)
    
    valStr = ", ".join(valStrList)
    sql = "UPDATE "+relName+" SET "+valStr
    if(where!=""):
        sql += " WHERE "+where
    sql += ";"

    for attr in tempAttr:
        for val in pkVal:
            tempRelName = "hist_"+dbName+"_"+relName+"_"+attr[0]
            sql += "UPDATE "+tempRelName+" SET ed_"+attr[0]+" = '"+today+"' WHERE "+pk[0]+" = "+str(val)+" AND ed_"+attr[0]+" IS NULL;"
            sql += "INSERT INTO "+tempRelName+" ("+pk[0]+", sd_"+attr[0]+", "+attr[0]+") VALUES ("+str(val)+", '"+today+"', "+str(attr[2])+");"
    
    print(sql)
    
    try:
        conn = CreateConnToExternalDB(dbFolder, dbFullName)
        curs = conn.cursor()
        for query in sql.split(";"):
            curs.execute(query)
        conn.commit()
        conn.close()
    except Error as e:
        conn.rollback()
        print(e)
        return 0
    return 1