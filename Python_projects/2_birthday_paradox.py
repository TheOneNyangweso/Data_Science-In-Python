"""
The birthday paradox - an example of a Monte Carlo experiment
"""
import datetime
import random

MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "June",
    "July",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)


def get_birthdays(no_of_bds):
    """
    Return a list of random birthdays
    """
    birthdays = []
    for i in range(no_of_bds):
        start_of_year = datetime.date(2001, 1, 1)
        rand_days = datetime.timedelta(random.randint(0, 364))

        birthday = start_of_year + rand_days
        birthdays.append(birthday)

    return birthdays


def get_match(birthdays):
    """
    Return the date object of a birthday that has occured more than once
    """
    # Check if all birthdays are unique
    if len(birthdays) == len(set(birthdays)):
        return None

    for a, birthday_A in enumerate(birthdays):
        for b, birthday_B in enumerate(birthdays[a + 1 :]):
            if birthday_A == birthday_B:
                return birthday_A


print('The birthday paradox - an example of a Monte Carlo experiment')
print(f'More info at https://en.wikipedia.org/wiki/Birthday_problem\n\n')

session = True
while session:
    print("How many birthdays should I generate? (Max 100)")
    response = input(">>> ")
    if response.isdecimal() and (0 < int(response) <= 100):
        num_of_birthdays_gen = int(response)
        break

print(f"\nHere are {num_of_birthdays_gen} birthdays")
birthdays = get_birthdays(num_of_birthdays_gen)
for count, birthday in enumerate(birthdays):
    if count != 0:
        # Display a comma for each birthday after the first b_day
        print(", ", end="")
        
    month_name = MONTHS[birthday.month - 1]
    date_text = f"{month_name} {birthday.day}"
    print(date_text, end="")

print()
print()

# find if there are matching b_days
match = get_match(birthdays)

print("In this simulation, ", end="")
if match != None:
    month_name = MONTHS[match.month - 1]
    date_text = f"{month_name} {match.day}"

    print(f"Multiple people have birthdays on {date_text}")
else:
    print(f"There are no matching birthdays\n")

# Run through 1000 simulations
print(f"Generating {num_of_birthdays_gen} random birthdays 1000 times...")
input("Press Enter to begin...")

sim_match = 0
for i in range(1000):
    # Report progress after every 100 simulations
    if i % 100 == 0:
        print(f"{i} simulations completed...")

    birthdays = get_birthdays(num_of_birthdays_gen)
    if get_match(birthdays) != None:
        sim_match += 1

print("1000 simulations completed!!")

# Display results
probability = round((sim_match / 1000) * 100, 2)
print(f"Out of 1000 simulations of {num_of_birthdays_gen} people,")    
print(f"There was a matching birthday in that group {sim_match} times. This means that {num_of_birthdays_gen}")
print(f"peoople have a {probability}% chance of having a matching birthday in their group!!")
