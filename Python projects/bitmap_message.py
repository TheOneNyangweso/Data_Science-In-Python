"""
BITMAP MESSAGE : A program to show how to work with multiline strings
In this bitmap, space characters represent an empty space, and all
other characters are replaced by characters in the user's message
"""
import requests
import sys

# Using requests to lazily download the bitmap.txt file...no need to type the whole prototype map
""" 
with open('/home/nyangweso/Desktop/Ds_1/Data_Structures/Python projects/bitmap.txt', 'w') as f:
    url = 'https://inventwithpython.com/bitmapworld.txt'
    response = requests.get(url).text
    
    f.write(response)
"""

# You can change the path to match that in your system
# open the bitmap.txt and save it in a variable
with open(
    "/home/nyangweso/Desktop/Ds_1/Data_Structures/Python projects/bitmap.txt", "r"
) as f:
    bitmap = f.read()

print("Bitmap message, by Sammy Moruri")

# Using a while to catch exceptions
while True:
    print("Enter the message to display with the bitmap")
    message = input(">> ")

    if message == "":
        print("Message can be empty, please try again...")
        # sys.exit()
    else:
        break
# Loop over each line in the bitmap:
for line in bitmap.splitlines():
    # Loop over each character in the line:
    for i, character in enumerate(line):
        if character == " ":
            # Print an empty space since the bitmap also contains a space
            print(" ", end="")
        else:
            # Print character from message:
            """
            The message[i % len(message)] causes the repetition of the input
            As i increases from 0 to a no. larger than len(message), the
            expression i % len(message) evaluates to 0 again.
            """
            print(message[i % len(message)], end="")

    print()
