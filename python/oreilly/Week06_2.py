import csv,os,uuid,hashlib,re
from datetime import datetime

userstable = None
sessiontable = []
updateatexit = False

def getUserId(username):
    global userstable
    return list(map(lambda r : r["id"] , list(userstable) ))[0]

def setSessionStatus(username, status):
    global sessiontable
    now = datetime.now()
    sessiontable.append({ "id": (len(sessiontable) + 1), "userid":getUserId(username),"status":status, "lastupdate": now})

def getUserSessionStatus(username):
    global sessiontable

    filteredbyuserid = list(filter(lambda s : s["userid"] == getUserId(username) , sessiontable))
    if len(filteredbyuserid) > 0:
       return list(sorted(filteredbyuserid, key= lambda i: i["id"], reverse=True))[0]
    else:
         return []

def savesession():
    if updateatexit == True:
        with open(file="auth.csv.new", mode="w+", newline="\n") as users:
            usrdbfile =  csv.writer(users, delimiter=",")
            #header
            usrdbfile.writerow( [value for value in userstable[0]] )
            for user in userstable:
                usrdbfile.writerow( [usrinfo for usrinfo in dict(user).values()] )
        os.system("mv auth.csv auth.csv.backup")
        os.system("mv auth.csv.new auth.csv")

def addUser(user):
    global userstable, updateatexit
    updateatexit = True
    tmptble = [row for row in userstable]
    tmptble.append(user)
    userstable = None
    userstable = tuple(tmptble)

def getkey(mapping, index):
    for v in mapping:
         if list(dict(v).keys())[0] == index:
            return dict(v).get(index)
def dbinit():

     global userstable
     initusrtable = []

     with open(file="auth.csv", mode="r", newline="\n") as users:
        usrdbfile =  csv.reader(users, delimiter=",")
        fieldstomap = None
        users = []
        #userdict = {}
        for row in usrdbfile:
            if usrdbfile.line_num == 1:
                fielndstomap = [ {item[0] : item[1] } for item in enumerate(row)]
            else:
                users.append(dict((getkey(fielndstomap,item[0]), item[1]) for item in enumerate(row)))
                #dict((y, x) for x, y in t)
        userstable = tuple(users)

     with open(file="sessions.csv", mode="r", newline="\n") as session:
        usersession =  csv.reader(session, delimiter=",")
        fieldstomap = None
        session = []
        for row in usersession:
            if usersession.line_num == 1:
                fielndstomap = [ {item[0] : item[1] } for item in enumerate(row)]
            else:
                session.append(dict((getkey(fielndstomap,item[0]), item[1]) for item in enumerate(row)))
        sessiontable = tuple(session)

def logginscree():
    
    print("Enter Credentials")
    username = input("Username: ")
    pwd = input("Password: ")
    pwd = hashlib.md5(pwd.encode()).hexdigest()
    return ({"username": username, "password":pwd})

def authenticate(credential):

    global userstable

    username = credential["username"]
    pwd = credential["password"]

    if username not in list(map(lambda r : r["username"] , list(userstable) )):
        return False
    else:
        os.system("clear")
        userinfo = list(filter(lambda r : r["username"] == username , list(userstable) ))[0]

        if userinfo["password"] == pwd:
            return True
        else:
            print("Invalid Password")
    return False
def logout():
    print("Logout")

def register():
    password = None
    os.system("clear")
    print("=" *65)
    print("= " + "{:<63}".format("Registration") + "=")
    print("=" *65)
    username=input("User Name: ")
    password1=input("Password: ")
    password2=input("Reenter Password: ")

    if username.lower() not in userstable:
        if password1 == password2:
            password = hashlib.md5(password1.encode()).hexdigest()
        else:
            os.system("clear")
            print("Password don't match")
            register()
        id = uuid.uuid5(uuid.NAMESPACE_DNS, username.lower())
        newuser = {"id" : id, "username": username, "password" : password}
        addUser(newuser)

def resetPassword():
    pass
def main(message, KeyHandler=None):

    global sessiontable

    os.system("clear")
    print("=" * 65)
    print("*"+"Welcome!".center(63)+"*")
    if message is not None:
        for line in str(message).split("\n"):
            print("*"+ line.center(63) +"*") 
    else:
        print("*"+ " ".center(63) +"*")     
    print("*"+ "L) Login | P) Password Rest | R) Register | E) Exit".center(63) +"*") 
    print("=" * 65)
    action = input("Action: ")
    

    if action.lower() == "l":
        credentials = logginscree()
        status = authenticate(credentials)
        if status is False:
            return {"code": False, "message":"Unable to authenticate user"}
        else:
            session = getUserSessionStatus(credentials["username"])
            if len(session) > 0: #and session["status"].lower() == "open":
                return {"code": False, "message":"{0} session open since {1}!\nWould you like to (Lo)Logout or Exist?".format(credentials["username"],session["lastupdate"]),"KeyHandler": "lo"}
            else:
                setSessionStatus(credentials["username"],"OPEN")
                return {"code": False, "message":"{0} has been authenticated!".format(credentials["username"])}
                
    elif action.lower() == "p":
        pass
    elif action.lower() == "r":
         register()
         return {"code": False, "message":"User Registration Sucessful!"}
    elif action.lower() == "e":
        savesession()
        return {"code":True,"message":None}
    elif KeyHandler != None:
        if keyhandler.lower() == "lo":
            return {"code":True,"message":"Bye!"}
    return  {"code":False,"message":"Invalid Option!"}
    
if  __name__ == "__main__":
    dbinit()
    status =  False
    returnstatus = {"code": None, "message":None}
    keyhandler = None
    while status is False:
        returnstatus = main(returnstatus["message"],keyhandler)
        status = returnstatus["code"]
        keyhandler = returnstatus.get("KeyHandler",None)
        