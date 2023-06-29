"""
Blackjack, also known as 21, is a card game where players try
to get as close to 21 points as possible without going over.
This Program is an example of how ASCII can create art (ASCII art)

More info at https://en.wikipedia.org/wiki/Blackjack
"""

print()

file = '/home/nyangweso/Desktop/Ds_1/Data_Structures/Python projects/4_blackjack/Rules.txt'
with open(file, 'r') as f:
    print(f.read())