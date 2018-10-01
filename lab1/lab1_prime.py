from time import sleep
from random import randint


class Agent:

    def __init__(self, number):
        self.number = number
        self.name = "Agent" + str(number)
        # print(self.number)

    def action(self, allnumber):
        delete_num = []
        for n in allnumber:
            if n % self.number == 0 and n != self.number:
                allnumber.remove(n)
                delete_num.append(n)

        print("Name: {},  Action: Remove {}".format(self.name, delete_num))

        
                

    

def gen_correct_res(number):
    num = []
    for i in range(2,number):
        j = 2 
        for j in range(2, i):
            if i%j == 0 :
                break
        else:
            num.append(i)
    return num


def sos(n):
    numbers = [i + 1 for i in range(n)]
    numbers.remove(1)
    # print(numbers)
    prime = gen_correct_res(n)
    # print(prime)
    agents = [Agent(i) for i in prime]
    # print(agents)
    while True:
        print("Current Numbers: {} ".format(numbers))
        index = randint(0,len(prime)-1)
        agents[index].action(numbers)
        sleep(1)
        if numbers == prime:
            print("OK")
            break
    
if __name__ == '__main__':
    n = 10
    sos(n)

    