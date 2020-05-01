import csv,os,uuid,hashlib,re
from datetime import datetime

userstable = None
sessiontable = None
updateatexit = False

def getUserId(username):
    global userstable
    user = list(filter(lambda r : r["username"] == username , list(userstable) ))
    if len(user) > 0:
        return user[0]["id"]
    else:
        return None

def setSessionStatus(username, status):
    global sessiontable
    now = datetime.now()
    
    mysession = list(filter(lambda s: dict(s)["userid"] == getUserId(username)  , sessiontable))
    if len(mysession) > 0:
        mysession[0]["status"] = status
    else:
        sessiontable.append({ "id": (len(sessiontable) + 1), "userid":getUserId(username),"status":status, "lastupdate": now})

def getUserSessionStatus(username):
    global sessiontable

    filteredbyuserid = list(filter(lambda s : s["userid"] == getUserId(username) , sessiontable))
    if len(filteredbyuserid) > 0:
       return list(sorted(filteredbyuserid, key= lambda i: i["id"], reverse=True))[0]
    else:
         return []

def savesession():

    global userstable,sessiontable

    if updateatexit == True:
        with open(file="auth.csv.new", mode="w+", newline="\n") as users:
            usrdbfile =  csv.writer(users, delimiter=",")
            #header
            usrdbfile.writerow( [value for value in userstable[0]] )
            for user in userstable:
                usrdbfile.writerow( [usrinfo for usrinfo in dict(user).values()] )
        os.system("mv auth.csv auth.csv.backup")
        os.system("mv auth.csv.new auth.csv")
    
    '''Save session status'''
    with open(file="sessions.csv.new", mode="w+", newline="\n") as session:
        usersession = csv.writer(session, delimiter=",")
        #header
        usersession.writerow([value for value in sessiontable[0]] )
        for session in sessiontable:
                usersession.writerow( [session for session in dict(session).values()] )
        os.system("mv sessions.csv sessions.csv.backup")
        os.system("mv sessions.csv.new sessions.csv")

def addUser(user):
    global userstable, updateatexit
    updateatexit = True
    tmptble = [row for row in userstable]
    tmptble.append(user)
    userstable = None
    userstable = [row for row in tmptble]

def getkey(mapping, index):
    for v in mapping:
         if list(dict(v).keys())[0] == index:
            return dict(v).get(index)
def dbinit():

     global userstable,sessiontable

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
        sessiontable = [s for s in session]

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

def resetPassword(msg=None):
    global userstable, updateatexit
    updateatexit = True
    password = None
    os.system("clear")
    print("=" *65)
    print("= " + "{}".format("{}".format("Password Rest") + (f": {msg}" if msg != None else "")).center(62) + "=")
    print("= "+ "{:<62}".format("B) Back") + "=") 
    print("=" *65)
    username=input("User Name: ")
    if username.lower() == "b":
        return False
    usercheck = list(filter(lambda u: u["username"] == username.lower(), userstable))
    
    password1=input("New Password: ")
    password2=input("Reenter New Password: ")
    if username.lower() == "b":
        return False

    if len(usercheck) == 1:
        if password1 == password2:
            password = hashlib.md5(password1.encode()).hexdigest()
        else:
            os.system("clear")
            passwordrest("Password don't match")
        usercheck[0]["password"] = password
    else:
        os.system("clear")
        passwordrest("User already exists!")

def register(msg=None):
    password = None
    os.system("clear")
    print("=" *65)
    print("= " + "{}".format("{}".format("Registration") + (f": {msg}" if msg != None else "")).center(62) + "=")
    print("= "+ "{:<62}".format("B) Back") + "=") 
    print("=" *65)
    username=input("User Name: ")

    if username.lower() == "b":
        return False

    password1=input("Password: ")
    password2=input("Reenter Password: ")

    if username.lower() == "b":
        return False
    usercheck = list(filter(lambda u: u["username"] == username.lower(), userstable))


    if len(usercheck) == 0:
        if password1 == password2:
            password = hashlib.md5(password1.encode()).hexdigest()
        else:
            os.system("clear")
            register("Password don't match")
        id = uuid.uuid5(uuid.NAMESPACE_DNS, username.lower())
        newuser = {"id" : id, "username": username.lower(), "password" : password}
        addUser(newuser)
    else:
        os.system("clear")
        register("User already exists!")

def main(**kwargs):

    global sessiontable
    message = kwargs["Message"]
    refusername = kwargs["Username"]
    KeyHandler = kwargs["Keyhandler"]

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
            return {"code": False, "Message":"Unable to authenticate user"}
        else:
            session = getUserSessionStatus(credentials["username"])
            if len(session) > 0 and session["status"].lower() == "open":
                return {"code": False, "Message":"{0} session open since {1}!\nWould you like to (Lo)Logout or Exist?".format(credentials["username"],session["lastupdate"]),"Keyhandler": "lo", "Username": credentials["username"]}
            else:
                setSessionStatus(credentials["username"],"OPEN")
                return {"code": False, "Message":"{0} has been authenticated!".format(credentials["username"])}
                
    elif action.lower() == "p":
        resetPassword()
    elif action.lower() == "show":
        return {"code" : False, "Message" : sessiontable}
    elif action.lower() == "r":
         status = register()
         if status !=  False:
            return {"code": False, "Message":"User Registration Sucessful!"}
         else:
             return {"code": False, "Message":"Registration Cancelled!"}
    elif action.lower() == "e":
        savesession()
        return {"code":True,"Message":None}
    elif KeyHandler != None:
        if KeyHandler.lower() == "lo":
            setSessionStatus(refusername,"CLOSED")
            return {"code":False,"Message":f"Logging off {refusername}!"}

    return  {"code":False,"Message":"Invalid Option!"}
    
if  __name__ == "__main__":
    dbinit()
    status =  False
    returnstatus = {}
    while status is False:
        returnstatus = main(
            Message=returnstatus.get("Message",None),
            Keyhandler=returnstatus.get("Keyhandler",None),
            Username=returnstatus.get("Username",None))
        status = returnstatus["code"]
        