from django.conf import settings
import sqlite3
from sqlite3 import Error
from sqlite3 import connect

def CreateConn(dbName):
    if(dbName==""):
        dbName = settings.DATABASES['default']['NAME']
    try:
        con = sqlite3.connect(dbName)
        return con
    except Error as e:
        print(e)
    return None

def CreateTable(con, query):
    try:
        cur = con.cursor()
        cur.execute(query)
    except Error as e:
        print(e)
        return 0
    return 1
    
'''
def Exec(query, values): #insert
    try:
        con = CreateConn()
        if(con==None):
            return 0
        cur = con.cursor()
        cur.execute(query, values)

def Fetch(query): #select
    con = CreateConn()
    if(con==None):
        return 0
    cur = con.cursor()
    cur.execute(query)
    cur.fetchall()
    con.close()
'''
def CreateNonTempTable(dbName, nonTempAttr):
    con=CreateConn("")
    if(con==None):
        return 0
    tableName = str(dbName)+"_nonTemp"
    sql = "CREATE TABLE '"+tableName+"' ( id INTEGER NOT NULL, "
    for attr in nonTempAttr:
        dt = ""
        if(attr[2]==0):
            dt = "INTEGER"
        elif(attr[2]==1):
            dt = "TEXT"
        if(attr[3]==True):
            dt += " NOT NULL"
        if(attr[4]==True):
            dt += " UNIQUE"
        sql+=attr[1]+" "+dt+", "
    sql = sql[:-2]+" )"
    print(sql)
    return CreateTable(con, sql)

def CreateTempTable(dbName, tempAttr):
    con = CreateConn("")
    if(con==None):
        return 0
    tableName = str(dbName)+"_"+tempAttr[1]
    sql = "CREATE TABLE '"+tableName+"' ( id INTEGER NOT NULL, "
    sql += "start_date TEXT, "
    if(tempAttr[2]==0):
        dt = "INTEGER"
    elif(tempAttr[2]==1):
        dt = "TEXT"
    dt += " NOT NULL"
    sql += str(tempAttr[1])+" "+dt+", "
    sql += "end_date TEXT )"
    print(sql)
    return CreateTable(con, sql)
    
    
# working with external db //already present with end user

def CreateConnToExternalDB(dbFolder, dbName):
    dbPath = dbFolder+"/"+dbName
    print dbPath
    conn = connect(dbPath)
    curs = conn.cursor()
    return curs
    
def GetRelFromDB(dbFolder, dbName):
    curs = CreateConnToExternalDB(dbFolder, dbName)
    curs.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = []
    for tableName in curs.fetchall():
        tables.append(tableName[0])
    return tables

def GetAttrFromRel(dbFolder, dbName, relName):
    attrList = []
    curs = CreateConnToExternalDB(dbFolder, dbName)
    result = curs.execute("PRAGMA table_info('%s')" % relName).fetchall()
    column_names = zip(*result)[1]
    column_types = zip(*result)[2]
    for i in range(len(column_names)):
        col = column_names[i]
        if(not(col[:3]=="ed_" or col[:3]=="sd_")):
            attrList.append([column_names[i], column_types[i]])
    print(attrList)
    return attrList
    
def ExecuteQuery(dbFolder, dbName, query):
    curs = CreateConnToExternalDB(dbFolder, dbName)
    statement = query.split(";")
    try:
        for stmt in statement:
            print(stmt)
            curs.execute(stmt)
    except Error as e:
        print(e)
        return 0
    return 1

def AttrAlreadyTemp(dbFolder, dbName, tableName):
    curs = CreateConnToExternalDB(dbFolder, dbName)
    tables = GetRelFromDB(dbFolder, dbName)
    if(tableName in tables):
        return True
    return False