from django.conf import settings
import sqlite3
from sqlite3 import Error

def CreateConn():
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
    con=CreateConn()
    if(con==None):
        return 0
    tableName = str(dbName)+"_nonTemp"
    sql = "CREATE TABLE '"+ tableName +"' ( "
    for attr in nonTempAttr:
        dt = ""
        if(attr[2]==0):
            dt = "INTEGER"
        elif(attr[2]==1):
            dt = "TEXT"
        sql+=attr[1]+" "+dt+", "
    sql = sql[:-2]+" )"
    print(sql)
    return CreateTable(con, sql)

def CreateTempTable(dbName, tempAttr):
    con = CreateConn()
    if(con==None):
        return 0
    tableName = str(dbName)+"_"+tempAttr[1]
    sql = "CREATE TABLE '" + tableName + "' ( "
    sql += "start_date TEXT, "
    if(tempAttr[2]==0):
        dt = "INTEGER"
    elif(tempAttr[2]==1):
        dt = "TEXT"
    sql += str(tempAttr[1])+" "+dt+", "
    sql += "end_date TEXT )"
    print(sql)
    return CreateTable(con, sql)