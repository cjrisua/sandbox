""" Palindrome 
word = input("Enter word: ")
word = word.replace(" ","").lower()
palindrome = [ w for w in word if w is not " "]
palindrome.reverse()
wordchecker = False if False in list(map(lambda i: palindrome[i[0]] == i[1] , enumerate(word))) else True
print("Is a palindrome? {}".format(wordchecker) )

userdic = {"name":None, "age":None}
print("Enter: {0}".format(userdic.keys()))
for i in enumerate(userdic.keys()):
    value = input("{}: ".format(i[1].title()))
    userdic[i[1]] = value
print("{}".format(userdic))

"""
"""
import csv
pizza = [{'meatlover':  ['cheese', 'sausage', 'peppers']}, 
         {"margarita" : ['tomato sauce', 'basil', 'mozzarella']}]
test = [ "Ingredients for {0}: {1}".format(list(dict(t).keys())[0], str.join(",",list(dict(t).values())[0])) for t in pizza]
print("\n".join(test))


with open("test.csv", mode="w+", newline="\n") as f:
    write = csv.writer(f, delimiter=",")
    write.writerow([list(dict(row).keys())[0] for row in pizza])
""""
    