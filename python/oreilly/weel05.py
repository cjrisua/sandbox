# using args parameter to take in a tuple of arbitrary values
def outputData(name, *args):
      print( type(args) )
      for arg in args:
              print(arg)
outputData("John Smith", 5, True, "Jess")

# using kwargs parameter to take in a dictionary of arbitrary values
def outputData(**kwargs):
      print( type(kwargs) )
      print( kwargs[ "name" ] )
      print( kwargs[ "num" ] )
outputData(name = "John Smith", num = 5, b = True)