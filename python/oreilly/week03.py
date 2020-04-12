""" 
Week 3: User input & type converting
""" 

# Creating a Calculator

""" Final Design 
1. Ask user for the calculation they would like to perform
2. Ask the user for the numbers they would like to run the operation on.
 
3.Set up try/except clause for mathematical operation.
    a.Convert numbers input to floats.
    b.Perform operation and print result.
    c.If an exception is hit, print error.
"""
avilibaleoperations=[
    {"key":1, "operation":"add", "symbol": "+"},
    {"key":2, "operation":"substract", "symbol": "-"},
    {"key":3, "operation":"multiply", "symbol": "*"},
    {"key":4, "operation":"divide", "symbol": "/"}]

print("=" * 50)
print("\t\tCalculator")
print("*" *50)

keys = map(lambda x : " {})".format(x["key"]) + x["operation"], avilibaleoperations)
menuoptions = " \n".join(list(keys))
while True:
    try:
        print("Would you like to:")
        print(menuoptions)
        operation = input("Selection: ")
        selectedoption = list(filter(lambda o: o["key"]== int(operation), avilibaleoperations))[0]
        print("+" * 50)
        usermsg = "+\tYou Selected: {0}".format(selectedoption["operation"]).ljust(44," ")
        print(usermsg + "+")
        print("+" * 50)
        float = x,y = input("X="),input("Y=")
        result=eval("{0}{1}{2}".format(x,selectedoption["symbol"],y))
        print("~" * 50)
        print("~\tResult: {0}{1}{2}={3}".format(x,selectedoption["symbol"],y,result))
        print("~" * 50)
    except:
        print("!" * 50)
        print(f"! Invalid Option {operation}".ljust(49," ") + "!")
        print("!" * 50)