import csv,os,uuid,hashlib

userstable = None
updateatexit = False

def savesession():
    if updateatexit == True:
        with open(file="auth.csv.new", mode="w+", newline="\n") as users:
            usrdbfile =  csv.writer(users, delimiter=",")
            #header
            usrdbfile.writerow( [value for users in userstable for value in dict(users).keys()] )
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
        userdict = {}
        for row in usrdbfile:
            if usrdbfile.line_num == 1:
                fielndstomap = [ {item[0] : item[1] } for item in enumerate(row)]
            else:
                users.append(dict((getkey(fielndstomap,item[0]), item[1]) for item in enumerate(row)))
                #dict((y, x) for x, y in t)

     userstable = tuple(users)
     with open(file="sessions.csv", mode="r", newline="\n") as usrsession:
        usrsession =  csv.reader(usrsession, delimiter=",")

def logginscree():

    print("Enter Credentials")
    #print("Username: {}".format(dict(userinfo).get("username")))
    username = input("Username: ")
    pwd = input("Password: ")
    return (username,pwd)

def authenticate():

    logginscree()

    if username not in list(map(lambda r : r["username"] , list(userstable) )):
        register()
    else:
        os.system("clear")
        userinfo = list(filter(lambda r : r["username"] == username , list(userstable) ))[0]

        if userinfo["password"] == hashlib.md5(pwd.encode()).hexdigest():
            print(f"Welcome {username} you session is now Active")
        else:
            print("Invalid Password")

def logout():
    print("lLog out")

def register():
    password = None
    ans=input("Would you like to be registered?: (Yes/No) ")
    if ans.lower() == "yes" or ans.lower() == "y":
        username=input("User Name: ")
        password1=input("Password: ")
        password2=input("Reenter Password: ")

        if username.lower() not in userstable:
            if password1 == password2:
                password = hashlib.md5(password1.encode())
            else:
                os.system("clear")
                print("Password don't match")
                register()

            id = uuid.uuid5(uuid.NAMESPACE_DNS, username.lower())
            newuser = {"id" : id, "username": username, "password" : password.hexdigest()}
            addUser(newuser)
            login(newuser["username"])
def main():
    os.system("clear")
    print("=" * 65)
    print("Welcome:")
    exitloop = True
    authenticate()
        
    
if  __name__ == "__main__":
    dbinit()
    main()