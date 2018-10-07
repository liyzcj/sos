from time import sleep
from random import randint


class Agent:

    def __init__(self, number):
        self.number = number
        self.name = "Agent" + str(number)
        # print(self.number)

    def delete_one(self, all_number):
        delete_num = None
        for num in all_number:
            if num % self.number == 0 and num != self.number:
                all_number.remove(num)
                delete_num = num
                break
        print("Name: {},  Action: Remove {}".format(self.name, delete_num))


def gen_correct_res(number):
    num = []
    for i in range(2, number):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            num.append(i)
    return num


def sos(g):
    numbers = [i + 1 for i in range(g)]
    numbers.remove(1)
    # print(numbers)
    prime = gen_correct_res(n)
    print("true prime ={} ".format(prime))
    # print(prime)
    agents = [Agent(i) for i in numbers]
    # print(agents)
    while True:
        print("Current Numbers: {} ".format(numbers))
        index = randint(0, len(prime)-1)
        agents[index].delete_one(numbers)
        sleep(1)
        if numbers == prime:
            print("numbers ==== {}".format(numbers))
            print("OK")
            break


if __name__ == '__main__':
    n = 30
    sos(n)
