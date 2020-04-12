#guessing game 
from random import randint
import subprocess as sup

guessed = False
number = randint(0,10)
guesses = 0

ans = input("\nTry to guess the number I am thinking of: ")
while not guessed:
    tmp = sup.call('clear', shell=True)
    guesses += 1
    if int(ans) == number:
        print ("Congrats! You guessed it correctly")
        print ("It took you {0} guesses! [{1}]".format(guesses,ans))
        break
    elif int(ans) > number:
        ans = input ("The number is lower than what you guessed - (answer): ")
    elif int(ans) < number:
        ans =input ("The number is greater than what you guessed - (answer): ")
    