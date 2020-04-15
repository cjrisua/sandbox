""" 
    Hangman Game!
"""
from random import choice

flagon,flagoff = 1, 0
words = [ "tree", "basket", "chair", "paper", "python" ]
word = choice(words)
guessed,lives, game_over = [], 7, False
print(" _?_ " * len(words))
hangman = [None] * len(words)
#print(word)
while not game_over:
    userletterguess = input("\nHow about guessing?: ")
    
    if userletterguess == "quit":
        game_over = True
        continue

    if userletterguess in word and userletterguess not in hangman and userletterguess.isalpha():
        guessed.append(userletterguess)
        hangman = list(map(lambda x: x if x == userletterguess or x in guessed else " ", list(word)))
        print(hangman)
        if " " not in hangman:
            print("Congratualtions!")
            game_over = True
    else:
        lives -= 1
        if lives == 0:
            game_over = True
            print(word)
        print(lives)
