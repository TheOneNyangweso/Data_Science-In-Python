import random


class Bagels():
    """
    Generates an n-digit number depending on the number of
    maximum digits passed
    Checks if user input a 3-digit number
    Checks if user input matches a generated 3-digit number
    """

    def __init__(self, num: str):
        # Assign to self object
        self.num = num
        self.rand_num = [a for a in range(0, 10, 1)]

    def generate_num(self):
        # generates random list to be used depending on
        # number of max digits
        return random.shuffle(self.rand_num)

    def checker(self):
        # Compares the user input and random number generated
        ls = []
        for count in range(0, 3, 1):
            for count_2 in range(0, 3, 1):
                if ord(self.rand_num[count]) == ord(self.num[count_2]):
                    ls.append("Fermi")
                elif ord(self.rand_num[count]) != (self.num[count_2]):
                    ls.append("Pico")
        count = 0
        for content in ls:
            if content.lower() == 'pico':
                count += 1
        if count == 3:
            print("Bagels")
        else:
            print(f"{' '.join(ls)}.")


if __name__ == '__main__':
    a = Bagels(100)
    a.generate_num()
    b = a.rand_num
    print(b[:3])
