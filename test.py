class A():
    def a(self):
        print('a')

class B(A):
    def b(self):
        self.a()

B().b()