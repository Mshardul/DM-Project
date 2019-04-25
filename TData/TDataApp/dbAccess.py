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
    print("-"*10)
    curs = (CreateConnToExternalDB(dbFolder, dbName)).cursor()
    result = curs.execute("PRAGMA table_info('%s')" % relName).fetchall()
    for r in result:
        if(r[5]==1):
            print(r[1])
            return (r[1], r[2])
    print("-"*10)
    
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
            return 1
        except Error as e:
            print(e)
            conn.rollback()
            return 0

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
        sql += "UPDATE "+tempRelName+" SET ed_"+attr[0]+" = '"+today+"' WHERE "+pk[0]+" = "+pkVal+"; "
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
    
def DeleteQuery(dbName, relNames, additionalRel, where): #helper.DeleteQuery()
    deleteRels =  ",".join(relNames)
    fromRels = ""
    if(len(additionalRel)==0):
        fromRels = deleteRels
    else:
        fromRels = deleteRels +","+ ",".join(additionalRel)
        
    sql = "DELETE "+deleteRels+" FROM "+fromRels
    if(where!=""):
        sql += " WHERE "+where
    print(sql)
    
    return 1

    