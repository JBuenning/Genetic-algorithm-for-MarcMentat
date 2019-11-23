class Test:
    def test_method(self,a):
        print(a)

class Tttest(Test):

    def test_metho123d(self,a,b):
        print(b)

t = Tttest()
t.test_method('Hallo')