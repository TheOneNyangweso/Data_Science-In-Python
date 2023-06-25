#!/usr/bin/python3
from bagels_input import Bagels as bg

MAX_NUM = 3

with open('bagels.txt') as f:
    bg_file = f.read()
    print(bg_file)

bagels = True
while bagels:
    for count in range(1, 11, 1):
        print(f"Guess #{count}")
        num = (input("> "))

        # Running verification
        assert len(num) == 3, "You have entered more or less than 3 numbers"

        # Instantiating class Bagels...
        a = bg(num)

        # Generating random number based on max digits...
        rand_num = a.generate_num()
        rand_num = rand_num[:MAX_NUM]
        
        # Checking guess...
        a.checker()

        if count == 10:
            print("Game over!!")
            print(f"The correct number is {rand_num}")

    print("Do you want to play again ? (Yes or No)")
    choice = input("> ")
    if choice.lower() == 'yes':
        continue
    elif choice.lower() == 'no':
        print("Thank you for playing.")
        bagels = False
