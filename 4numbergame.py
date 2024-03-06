# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:23:48 2023

@author: ryand
"""

import random

def n_place(pins, guess):
    
    return sum(1 for p, g in zip(pins, guess) if p == g)

def n_color(pins, guess):
    count = sum(min(guess.count(color), pins.count(color)) for color in set(guess))
    count2 = count - n_place(pins, guess)
    return count2

def getPins():
    """Generate four random pins with different colors."""
    pins = ''.join(str(random.randint(1, 6)) for _ in range(4))
    while len(set(pins)) < 4:
        pins = ''.join(str(random.randint(1, 6)) for _ in range(4))

    return pins


def PlayGame():
    play_again = 'y'
    
    while play_again == 'y':
        secret_pins = getPins()
    
        guesses = 10
        
        print("")
        while guesses > 0:
            guess = input("Guess 4 different colors: ")
            
            correct_place = n_place(secret_pins, guess)
            correct_color = n_color(secret_pins, guess)
            
            print(f"{correct_place} on correct place, {correct_color} with correct color")
            
            if correct_place == 4:
                print("You have won!")
                break
            
            # Decrement guesses left
            guesses -= 1
            print(f"Guesses left: {guesses}")
            
            if guesses == 0:    
                # Display the correct pins if Player 2 lost
                print(f"You have lost. The correct pins were: {secret_pins}")
    
        print("")
        print("")   
        # Ask if the player wants to play again
        play_again = input("Do you want to play once more? [y or n]: ").lower()


PlayGame()