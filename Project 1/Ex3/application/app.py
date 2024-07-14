# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os,io,nltk,re
nltk.download('punkt')
nltk.download('stopwords')
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql as db
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words=nltk.corpus.stopwords.words('english')
new_stopwords=["i", "x", "patient", "vaccine", "covid", "injection", "hours", "arm", "site", "medical", "history", "concomitant", "vital","hr",\
    "took", "day", "left", "went", "symptoms", "body", "felt","severe", "received","took", "tylenol", "single", "dose", "outcome","rr", "via", \
    "dose", "started", "feeling", "right", "first", "unspecified", "within", "heart" , "medications", "route", "reported", "event","lot","batch",  \
    "around","developed", "red", "days", "hives", "back", "morning","prior", "area", "signs", "spo", "diphenhydramine", "famotidine", "administered",\
    "report", "minutes", "hospital","pm", "mg", "spontaneous", "contactable", "pfizer", "bntb", "biontech", "feb", "th", "emergency", "administration",\
    "jan", "unknown", "information", "grade", "number", "taken", "lymph", "node", "extremity", "vitamin", "age", "immunization", "getting", "became",\
    "orally", "observed", "quickly", "began", "better", "disappeared", "coworkers", "altered", "mental","status", "sided", "see", "given", "h",\
    "onset"]
stop_words.extend(new_stopwords)


def connection():
    ''' User this function to create your connections '''
    con = db.connect(
        host =settings.mysql_host, 
        user =settings.mysql_user, 
        password= settings.mysql_passwd, 
        db =settings.mysql_schema)
    
    return con

def mostcommonsymptoms(vax_name):
    #ekteleite gia pfizer kai epistrefei ta top 10 sumptomata
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    sql="SELECT symptoms FROM vaccination, vaccines WHERE vaccines.vax_name=%s AND vaccines.vax_name = vaccination.vaccines_vax_name"
    cur.execute(sql, vax_name)
    result=cur.fetchall()
    
    res = [element for tupl in result for element in tupl]
    new_res=''.join(res)
    new_result=create_ngrams(new_res, 1)                                                #peira thn idea apo edw https://stackoverflow.com/questions/3594514/how-to-find-most-common-elements-of-a-list?fbclid=IwAR0T9hji3ChFidX7sJSf_geyW1zMMmz3f98RV91RbGBP1_YnDSetE6pnAEo
    clean_word_list=[word for word in new_result]
    word_counter={}
    for word in clean_word_list:
        if word in word_counter:
            word_counter[word]+=1
        else:
            word_counter[word]=1
    popular_words= sorted(word_counter, key= word_counter.get, reverse=True)
    top_10=popular_words[:10]
                              

    return [("vax_name","result"), (vax_name, top_10)]

def create_ngrams(s, n):
    # Convert to lowercases
    s=s.lower()
    
    # Replace all none alphanumeric characters with spaces
    s=re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    s=re.sub(r'[0-9]','', s)

   
    # Break sentence in the token, remove empty tokens
    tokens=[token for token in s.split(" ") if token != ""]
    temp=[word for word in tokens if word not in stop_words]
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams=zip(*[temp[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def combine(num1,num2):
    digits = len(str(num2))
    num1 = num1 * (10**digits)
    num1 += num2
    return num1

def buildnewblock(blockfloor):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    

    sql = ''' 
    select distinct block.blockfloor from block
    ''' 

    cur.execute(sql)

    table=cur.fetchall()
    floor = list()
    for row in table:
        floor.append(row[0])
    if int(blockfloor) not in floor:
        return[("Floor does not exist")]

    sql2 = ''' select block.blockcode from block where block.blockfloor = %s
    ''' 
    
    cur.execute(sql2, blockfloor)

    table=cur.fetchall()
    code = list()

    for row in table:
        code.append(row[0])

    count = 0 
    for i in code:
        count += 1 

    if count == 9:
        return [("Floor cant have any more blocks")]
    else:

        temp = list()

        for i in range (1,10):
            if i not in code:
                temp.append(i)

        newblock = random.choice(temp)
        roomnum=list()
        random4=random.randint(1,5)
        for i in range (random4):
            roomnum.append((int(blockfloor) * 1000) + (newblock * 100)+ i)
           
        roomtype=list()
        Available=list()
        for i in range(random4):
            random2 = random.randint(0,4)
            if random2 == 0:
                roomtype.append('single')
            elif random2 == 1:
                roomtype.append('double')
            elif random2 == 2:
                roomtype.append('triple')
            else:
                roomtype.append('quadruple')
            
            random3 = random.randint(0,1)
            if random3 == 0:
              Available.append(0)
            else:
              Available.append(1)            
        
        result = 'ok'
        sql="""INSERT INTO block (BlockFloor, BlockCode)
                    VALUES (%s, %s)"""        
        cur.execute(sql, (blockfloor, newblock))
        
        
        #table= cur.fetchall()
       # cur.execute(sql4,newblock)
       # table= cur.fetchall()
        sql="""INSERT INTO room (RoomNumber, RoomType, BlockFloor, BlockCode,Unavailable)
                VALUES (%s, %s, %s, %s, %s)"""
        for i in range(random4):
            cur.execute(sql, (roomnum[i], roomtype[i], blockfloor, newblock, Available[i] ))
       # sql="Select * From room Where room.BlockFloor= %s AND room.BlockCode=%s"
       # cur.execute(sql, (blockfloor, newblock))
       # results=cur.fetchall()
       # for row in results:                #ektelontas auto blepw oti ta room exoun ftiaxtei alla den emfanizonte sthn
       #     print(row)                     #bash an kanw query sthn mysql   
            
    return [("result",result)]

def findnurse(x,y):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    sql= "Select  distinct n.Name ,n.EmployeeID , o.BlockCode \
        From nurse n, on_call o Where o.BlockFloor = %s"
    cur.execute(sql, x)
    results=cur.fetchall()
    nurse_name=list()
    nurse_id= list()
    temp=list()
    temp1=list()
    for row in results:
            nurse_name.append(row[0])
            nurse_id.append(row[1])
    sql= "Select distinct o.BlockCode From on_call o Where o.BlockFloor=%s"
    cur.execute(sql, x)
    results= cur.fetchall()
    blocks=len(results)
    current_name=nurse_name[0]
    next_name=nurse_name[0]
    i=1
    count=0
    while i < len(nurse_name) :
        if current_name==next_name:
            count+=1
        else:
            count=0
        if count==blocks:
                temp.append(nurse_name[i-1])
                temp1.append(nurse_id[i-1])
                count=0
                current_name=nurse_name[i]
                next_name=nurse_name[i]
                i+=1
                continue
        current_name=next_name
        next_name=nurse_name[i]    
        i+=1
    nurse_name=temp
    nurse_id=temp1
    sql="Select a.PrepNurse From appointment a order by a.PrepNurse"
    cur.execute(sql)
    results=cur.fetchall()
    appointments=list()
    for row in results:
        appointments.append(row[0])
    temp=list()
    temp1=list()
    for i in range(len(nurse_id)):
        count=0
        for j in range(len(appointments)):
            if nurse_id[i]==appointments[j]:
                count+= 1
        if count >= int(y):
            temp.append(nurse_name[i])
            temp1.append(nurse_id[i])
    nurse_name=temp
    nurse_id=temp1
    sql="Select v.nurse_EmployeeID From vaccination v"
    cur.execute(sql)
    results=cur.fetchall()
    vaccinations=list()
    for row in results:
        vaccinations.append(row[0])
    num_of_patients=list()
    for i in range(len(temp1)):
        count=0
        for j in range(len(vaccinations)):
            if nurse_id[i]==vaccinations[j]:
                count+=1
        num_of_patients.append(count)
    return [("Nurse", "ID", "Number of patients"),(nurse_name, nurse_id, num_of_patients)]

def patientreport(patientName):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    sql="Select ph.Name From patient p, undergoes u, physician ph \
        Where  p.Name=%s AND p.SSN=u.Patient AND u.Physician=ph.EmployeeID"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Physician=list()
    for row in results:
        Physician.append(row[0])
    sql="Select n.Name From patient p, undergoes u, nurse n \
        Where p.Name=%s AND p.SSN=u.Patient AND n.EmployeeID=u.AssistingNurse"
    cur.execute(sql, patientName)
    results=cur.fetchall() 
    Nurse=list()
    for row in results:
        Nurse.append(row[0])
    sql="Select s.StayEnd From patient p, undergoes u,stay s  \
        Where p.Name=%s AND p.SSN=u.Patient AND s.StayID=u.Stay"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Date_Of_Release=list()
    for row in results:
        Date_Of_Release.append(row[0])
    sql="Select t.Name From patient p, undergoes u,treatment t  \
        Where p.Name=%s AND p.SSN=u.Patient AND u.Treatment=t.Code"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Treatment_Going_On=list()
    for row in results:
        Treatment_Going_On.append(row[0])
    sql="Select t.Cost From patient p, undergoes u, treatment t  \
        Where p.Name=%s AND p.SSN=u.Patient AND u.Treatment=t.code"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Cost=list()
    for row in results:
        Cost.append(row[0])
    sql="Select r.RoomNumber From patient p, undergoes u, stay s, room r  \
        Where p.Name=%s AND p.SSN=u.Patient AND u.Stay=s.StayID AND s.Room=r.RoomNumber"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Room=list()
    for row in results:
        Room.append(row[0])
    sql="Select r.BlockFloor From patient p, undergoes u, stay s, room r  \
        Where p.Name=%s AND p.SSN=u.Patient AND u.Stay=s.StayID AND s.Room=r.RoomNumber"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Floor=list()
    for row in results:
        Floor.append(row[0])
    sql="Select r.BlockCode From patient p, undergoes u, stay s, room r  \
        Where p.Name=%s AND p.SSN=u.Patient AND u.Stay=s.StayID AND s.Room=r.RoomNumber"
    cur.execute(sql, patientName)
    results=cur.fetchall()
    Code=list()
    for row in results:
        Code.append(row[0])

    return [("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block"),(patientName,Physician,Nurse,Date_Of_Release,Treatment_Going_On,Cost,Room,Floor,Code)]

