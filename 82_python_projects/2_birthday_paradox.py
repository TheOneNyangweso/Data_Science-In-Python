"""
The birthday paradox - an example of a Monte Carlo experiment
"""
import datetime
import random

MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

def get_birthdays(no_of_bds):
    """
    Return a list of random birthdays
    """
    pass
def get_match(birthdays):
    """
    Return the date object of a birthday that has occured more than once
    """
    pass

while True:
    print('How many birthdays should I generate? (Max 100)')
    response = int(input('>>> '))
    if response.isdecimal() and (0 < response <= 100):
        num_of_birthdays_gen = response
        break
    
