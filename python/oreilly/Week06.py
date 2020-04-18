""" Basic Python Shopping Cart """
import curses, os
inventory=[
    {"wine": "D'Angerville"},
    {"wine": "Colombine"}, 
    {"food": "Jamonilla"},
    {"food" : "flower"}, 
    { "beer" :"Corona Light"}]
selectionmap = []
suboption = 'a'
alertflag = False

def UIheader():

    os.system("clear")
    print("Welcome to TabinColmadoe")
    print("Items for Sale:")

def displayItemsToBuy(selection, filterbyitem = None):

    selectionkey = list(filter(lambda x: x["optionidx"] == str(selection), selectionmap))[0]
    
    uniquecategories = list(filter(lambda x: dict(x).keys().__contains__(selectionkey["item"]), inventory))
    
    if filterbyitem is not None:
        uniquecategories = [a for a in uniquecategories if a[selectionkey["item"]] == filterbyitem]

    print((" "*2) + "[{}] {}".format(selectionkey["optionidx"], selectionkey["item"].title()))
    for index,item in enumerate(uniquecategories):
        print((" ")*5+"[{0}] {1}".format(chr(ord(suboption)+index),item[selectionkey["item"]].title()))
        selectionmap.append({"optionidx":chr(ord(suboption)+index), "item" :item[selectionkey["item"]], "itemcategory" : selectionkey["optionidx"]})

def userSelectionOption():
    option=list(filter(lambda x: dict(x).get("category") == "yes", selectionmap))
    if len(option) == 1:
        return option[0]["optionidx"]
    return None

def ProductPurchaseOption(selection):

    UIheader()

    subitemselection = dict(selection).get("item")
    displayItemsToBuy(dict(selection).get("itemcategory"), subitemselection)

    action= input("\nWould you like to purchase this item?(Yes/No) ")

    if action.lower().__contains__("y"):
        #Add Item to Shopping List
        pass
    else:
        #Do Nothing
       pass

def showUI(selection=None):

    mainmenue="(E)Exit | (S)Show Shopping Cart"
    
    UIheader()
   
    if selection is None:
        uniquecategories = list(set(val for dic in inventory for val in dic.keys())) 
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