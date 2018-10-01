import lib1

def compute(last_line):

    last_line.append(0)
    new_line = list(range(len(last_line)))

    for i in new_line:
        new_line[i] = last_line[i-1]+last_line[i]
        
    return new_line

# pascal = [[1]]
# for i in range(10):
    # pascal.append(compute(pascal[i][:]))

# for line in pascal:
    # print(line)
