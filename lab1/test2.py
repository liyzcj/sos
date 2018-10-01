class test:
    
    def add(self, x):
        x = [5]
    def action(self,x):
        self.add(x)

a = [[1],[2],[3]]

test = test()
x = a[2]
test.action(x)

print(a)
