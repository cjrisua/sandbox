import re
import locale


locale.setlocale(locale.LC_ALL,'')
#Comments & Basic Data Types
"""
Hello large commemnt area
"""
print("Carlos Rivera")
integer = 0
amount = 12.50
isactive = True

print("types: {0},{1},{2}".format(
    type(amount),
    type(integer),
    type(isactive)))

mystring = f"My integer of {amount}".upper()
print(mystring[17:12])

print(mystring)

"""
  Friday Project: Printing Receipts
"""
companyName = "coding temple, inc."
companyAddress = "283 Franklin St."
companyCity = "Boston, MA"


addToBasket=True
myShoppingBasket=[]
while addToBasket == True:
    articale_name, articale_price = input("Item: "), float(input("Price: "))
    myShoppingBasket.append([articale_name,articale_price])
    answer = input("Add More? (Y/N)")
    addToBasket = True if re.match("(Y|y|Yes|yes)", answer) else False
print("*" * 50)
print(f"\t\t{companyName}".title())
print(f"\t\t{companyAddress}".title())
print(f"\t\t{companyCity}")
print("=" * 50)
print(f"\tProduct Name\tProduct Price")
for basketitem in myShoppingBasket:
    print(" \t{0}\t ${1:,.2f}".format(
        basketitem[0].ljust(15," ").title(),
        basketitem[1]))

total = sum(map(lambda a : a[1], myShoppingBasket))
print("=" * 50)
print("\t\t\tTotal")
print("\t\t\t ${:,.2f}".format(total))
print("=" * 50)
print("\tThanks for shopping with us today!")
print("*" * 50)
