""" Basic Python Shopping Cart """
import curses, os, textwrap

shoppingcart=[]
inventory=[
    {"wine": "Domaine de la Romanée-Conti Romanee Conti", "data" : { "price": float(25030.99), "onstock" : "2" } },
    {"wine": "D'Angerville", "data" : {"price": float(130.99)} },
    {"wine": "Colombine", "data" : {"price": float(79.99)} },
    {"food": "Jamonilla", "data" : {"price": float(1.99)} },
    {"food": "flower", "data" : {"price": float(0.99) }},
    {"beer": "Corona Light", "data" : {"price": float(8.99)}},
    {"home essentials" : "Cottonelle Toilet paper", "data" : {"price" : float(7.99), "onsale" : float(15), "onstock" : 2, "restriction" : 1}}
    ]
selectionmap = []
suboption = 'a'
alertflag = False
alertmessage = ""

def removeItem():
    print("Remove???")

def getCategoryItem(optionindex):
    return list(filter(lambda x: x["optionidx"] == str(optionindex), selectionmap))[0]

def getPriceItem(category, item):
    return float(list(filter(
        lambda x : dict(x).keys().__contains__(category) and item in dict(x).values(), inventory))[0]["data"]["price"])
def UIheader():

    os.system("clear")
    print("=" *67)
    print("="+"Welcome to 'Colmado de Don Chucho'".center(65) + "=")
    print("*" *67)
    print(" Items for Sale:")

def displayItemsToBuy(selection, filterbyitem = None):

    selectionkey = list(filter(lambda x: x["optionidx"] == str(selection), selectionmap))[0]
    
    uniquecategories = list(filter(lambda x: dict(x).keys().__contains__(selectionkey["item"]), inventory))
    
    if filterbyitem is not None:
        uniquecategories = [a for a in uniquecategories if a[selectionkey["item"]] == filterbyitem]

    print(" " + (" "*2) + "[{}] {}".format(selectionkey["optionidx"], selectionkey["item"].title()))
    for index,item in enumerate(uniquecategories):
        print((" ")*5+"[{0}] {1:<38}\t${2:,.2f}".format(
            chr(ord(suboption)+index),
            textwrap.shorten(item[selectionkey["item"]].title().ljust(45," "), width = 35),
            getPriceItem(selectionkey["item"],item[selectionkey["item"]])))
        selectionmap.append({"optionidx":chr(ord(suboption)+index), "item" :item[selectionkey["item"]], "itemcategory" : selectionkey["optionidx"]})

def userSelectionOption():
    option=list(filter(lambda x: dict(x).get("category") == "yes", selectionmap))
    if len(option) == 1:
        return option[0]["optionidx"]
    return None

def ProductPurchaseOption(selection):
    global alertflag, alertmessage

    UIheader()

    subitemselection = dict(selection).get("item")
    category = dict(selection).get("itemcategory")
    displayItemsToBuy(category, subitemselection)

    action= input("Would you like to purchase '{}' item?(Yes/No) ".format(subitemselection))

    if action.lower().__contains__("y"):
        productcategory=getCategoryItem(category)
        shoppingcart.append(
            list(
                filter(
                    lambda x : dict(x).keys().__contains__(productcategory["item"]) and subitemselection in dict(x).values(),
                    inventory))[0])
        alertflag = True
        alertmessage = "Confirmation: Item added sucessfully!"
    else:
        #Do Nothing
       pass

def ShowUIShoppingCart():
    os.system("clear")
    print("=" * 60)
    print("Shopping Cart".center(60))
    print("=" * 60)
    uniquecategories = list(set(val for dic in shoppingcart for val in dic.keys() if val != "data" )) 

    totaldiscount = 0
    totalamount = 0
    for category in uniquecategories:
        print("{:<59}".format(textwrap.indent(category.title(), "+  ")) + "+")
        for item in [dic for dic in shoppingcart if category in dic.keys()]:
            discount = float(0)
            itemname = item[category]
            itemprice = item["data"]["price"]
            totalamount = totalamount + itemprice
            itemonsale = float(0 if "onsale" not in item["data"].keys()  else item["data"]["onsale"])
            if itemonsale > 0:
                discount = float(itemprice) - (float(itemprice) *  (float(itemonsale) /100))
                totaldiscount = totaldiscount + itemprice-discount
            line = "+" + "{0:<42}".format(textwrap.indent(textwrap.shorten(itemname.title().ljust(42," "), width = 35)," "*4))
            line = line + str("${:,.2f}".format(itemprice) + ("" if discount == 0 else " (-${:,.2f})".format(itemprice-discount))).ljust(16, " ")
            print("{0}".format(line.ljust(50," ")) + "+")
    print("=" * 60)
    print(" "*36 + "Total: ${:,.2f}".format(totalamount - totaldiscount))
    mainmenue="(E)Exit| (VS)Show Shopping Cart [{0}]| (Rm) Remove".format(len(shoppingcart))
    print(mainmenue)

def showUI(selection=None):

    global alertflag,alertmessage
    mainmenue="(E)Exit | (VS)Show Shopping Cart [{0}]".format(len(shoppingcart))
    
    UIheader()
   
    if selection is None:
        uniquecategories = list(set(val for dic in inventory for val in dic.keys() if val != "data" )) 
        for index, category in enumerate(uniquecategories):
            selectionmap.append({"optionidx" : str(index + 1), "item" : category, "category" : "yes" })
            print("  {0} {1}".format(index+1,category.title()))
        print(mainmenue)
    elif selection == "vs":
        ShowUIShoppingCart()
    else:
        try:
            #get user selection option
            selectionkey = list(filter(lambda x: x["optionidx"] == str(selection), selectionmap))[0]

            selectionmap.clear()
            #User Product Selection Only
            selectionmap.append(selectionkey)

            displayItemsToBuy(selection)

            mainmenue = mainmenue + " | (M)Main Menu"
            print(mainmenue)
        except:
            alertflag = True
            alertmessage = "Warning: Selected item {} Not Found".format(selection)
            showUI(userSelectionOption())

if __name__ == "__main__":
    useraction = None

    while True:
        showUI(useraction)

        if alertflag:
            print("{0}".format(alertmessage))
            alertflag = False

        useraction=input("Selction: ").lower()
        if useraction == "e":
            break
        elif useraction == "m":
            selectionmap = []
            useraction = None
        elif useraction.lower() == "vs":
            pass
        elif useraction.lower() == "rm":
            removeItem()
        else:
            try:
                #check for user selection
                optionidxitem =list(filter(lambda x: dict(x).get("optionidx") == str(useraction), selectionmap))
                if len(optionidxitem) == 0:
                    alertflag = True
                    alertmessage = "Warning: Selected item {} Not Found".format(optionidxitem)
                if optionidxitem[0]["optionidx"].isalpha():
                    #Shopping List Items
                    ProductPurchaseOption(optionidxitem[0])
                    #Set Flag back to product category
                    useraction = userSelectionOption()
            except:
                alertflag = True
                alertmessage = "Warning: Selected item {} Not Found".format(useraction)