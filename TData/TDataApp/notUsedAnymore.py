''' -------------------- views.py -------------------- '''

@csrf_exempt
def CreateRel(request): #used for 'createOp'
	print("="*20)
	
	data=json.loads(request.POST['data'])
	print(data)
	dbName = data['dbName']
	relName = data['relName']
	attributes = data['attributes']
	
	for attr in attributes: #[bool isTemp, string attrName,]
		attr[0] = True if int(attr[0])==1 else False
		attr[1] = str(attr[1])
		# attr[2] = int(attr[2])
		# attr[3] = True if int(attr[3])==1 else False
		# attr[4] = True if int(attr[4])==1 else False
	
	print(dbName)
	# print(relName)
	print(attributes)
	
	resp = createOp.Main(dbName, attributes) #deleted this file as well
	
	print("="*20)
	return HttpResponse(resp);
	

@csrf_exempt
def GetRel(request): #seems to be similar to GetRelList(). will verify later.
	print("="*20)
	
	dbName = json.loads(request.POST['dbName'])
	print dbName
	rels = helper.GetRels(dbName)
	print rels
	print("="*20)
	if rels==0:
		print("sending empty string")
		return HttpResponse("")
	else:
		print("sending list of relations")
		return HttpResponse(rels)

@csrf_exempt
def CheckRel(request):
	dbName = json.loads(request.POST['dbName'])
	relName = json.loads(request.POST['relName'])
	db_id, rel_id = helper.UniqueRel(dbName, relName)
	if(db_id==0):
		return HttpResponse("-1")
	elif(rel_id==0):
		return HttpResponse("1")
	else:
		return HttpResponse("0")
	
def DisplayAllDB(request):
	pass


@csrf_exempt
def GetDB(request): #seems to be similar to GetDBList(). will verify later.
	dbList = helper.GetAllDB()
	print(dbList)
	return HttpResponse(dbList)


''' -------------------- helper.py -------------------- '''

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
    
''' -------------------- dbAccess.py -------------------- '''

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
        con.commit()
    except Error as e:
        print(e)
        con.rollback()
        return 0
    return 1
    
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