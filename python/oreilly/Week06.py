""" Basic Python Shopping Cart """
import curses, os, textwrap

shoppingcart=[]
inventory=[
    {"wine": "Domaine de la Romanée-Conti Romanee Conti", "data" : { "price": float(25030.99) } },
    {"wine": "D'Angerville", "data" : {"price": float(130.99)} },
    {"wine": "Colombine", "data" : {"price": float(79.99)} },
    {"food": "Jamonilla", "data" : {"price": float(1.99)} },
    {"food": "flower", "data" : {"price": float(0.99) }},
    {"beer": "Corona Light", "data" : {"price": float(8.99)}}]
selectionmap = []
suboption = 'a'
alertflag = False

def getCategoryItem(optionindex):
    return list(filter(lambda x: x["optionidx"] == str(optionindex), selectionmap))[0]

def getPriceItem(category, item):
    return float(list(filter(
        lambda x : dict(x).keys().__contains__(category) and item in dict(x).values(), inventory))[0]["data"]["price"])
def UIheader():

    os.system("clear")
    print("=" *67)
    print("="+"Welcome to 'Colmade de Don Chucho'".center(65) + "=")
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
        print("Item added!")
    else:
        #Do Nothing
       pass

def showUI(selection=None):

    mainmenue="(E)Exit | (S)Show Shopping Cart [{0}]".format(len(shoppingcart))
    
    UIheader()
   
    if selection is None:
        uniquecategories = list(set(val for dic in inventory for val in dic.keys() if val != "data" )) 
        for index, category in enumerate(uniquecategories):
            selectionmap.append({"optionidx" : str(index + 1), "item" : category, "category" : "yes" })
            print("  {0} {1}".format(index+1,category.title()))
        print(mainmenue)
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
            showUI(userSelectionOption())

if __name__ == "__main__":
    useraction = None
    while True:
        showUI(useraction)

        if alertflag:
            print("Invalid Selection!!")
            alertflag = False

        useraction=input("Selction: ").lower()
        if useraction == "e":
            break
        elif useraction == "m":
            selectionmap = []
            useraction = None
        else:
            try:
                #check for user selection
                optionidxitem =list(filter(lambda x: dict(x).get("optionidx") == str(useraction), selectionmap))
                if len(optionidxitem) == 0:
                    alertflag = True
                if optionidxitem[0]["optionidx"].isalpha():
                    #Shopping List Items
                    ProductPurchaseOption(optionidxitem[0])
                    #Set Flag back to product category
                    useraction = userSelectionOption()
            except:
                 input("{0} is an Invalid Option!".format(useraction))