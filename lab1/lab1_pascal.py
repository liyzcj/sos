from random import randint
from time import sleep


class Agent:

    row_number = 0
    name = 'name'

    def __init__(self, row_number):

        self.row_number = row_number
        self.name = 'Agent' + str(row_number)

    def action(self, last_line):
        print('Name:{},  Location:Line{}, '.format(self.name, self.row_number), end=" ")

        if self.row_number == 1:
            new_line = [1]
            print("=[1]")
        elif not last_line:
            new_line = []
            print('Wait...')
        else:
            new_line = self.compute(last_line[:])
            print("compute {}".format(new_line))
        return new_line

    @staticmethod
    def compute(last_line):
        last_line.append(0)
        # calculate new line depends on last line.
        new_line = list(range(len(last_line)))
        for i in new_line:
            new_line[i] = last_line[i-1]+last_line[i]
        
        return new_line


'''
function : generate the correct result of pascal triangle
input  : n -- the number of line
output : A list contain each line of pascal triangle
'''


def gen_correct_res(row_number):

    pascal = [[1]]
    for i in range(row_number-1):
        pascal.append(Agent.compute(pascal[i][:]))
    return pascal


def sos(row_number):
    pascal = [[]] * row_number
    agents = [Agent(i) for i in range(1, row_number+1)]

    # print (agents)
    "generate the correct pascal triangle first"
    correct_res = gen_correct_res(row_number)
    # print(correct_res)
    # print(pascal)
    while True:
        "generate random number to simulate multi threading"
        i = randint(0, row_number - 1)
        last_line = pascal[i-1]
        "agent action"
        pascal[i] = agents[i].action(last_line)
        "compare with the correct result, stop when the result is same"
        if pascal == correct_res:
            break
        print("Pascal = {} ".format(pascal))
        sleep(1)
    print('ok')
    

if __name__ == '__main__':
    "generate correct pascal triangle"
    # pascal = gen_correct_res(10)
    # for line in pascal:
    # print(line)
    sos(6)
