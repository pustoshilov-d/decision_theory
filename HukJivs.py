import numpy as np
from math import *

class HukJivs(object):
    def __init__(self, n, h, d, m, e, f):
        self.f = f
        self.result = []
        self.n = n
        self.m = m
        self.e = e
        self.H =  np.array([h] * n)
        self.d = d
        self.X = np.array([0.0] * 3 * n).reshape(3, n)
        self.X[0] = np.array([0.0]*n)

    def explore(self):
        for i in range(self.n):
            self.X[1, i] = self.X[1, i]  + self.H[i]
            if self.f(self.X[1]) >= self.f(self.X[0]):
                self.X[1, i] = self.X[1, i] - 2 * self.H[i]
                if self.f(self.X[1]) >= self.f(self.X[0]):
                    self.X[1, i] = self.X[1, i] + self.H[i]

    def match(self):
        self.X[2] = self.X[1] + self.m * (self.X[1] - self.X[0])

    def eval(self):
        k =0
        Ostanov = False
        while not Ostanov:
            self.X[1] = self.X[0]
            self.explore()

            #удачен ли исслед поиск
            if self.f(self.X[1]) == self.f(self.X[0]):
                self.H /= self.d
                self.explore()
            else:
                self.match()

            #удачен ли поиск по образцу
            if self.f(self.X[2]) < self.f(self.X[1]):
                if self.f(self.X[2]) < self.f(self.X[0]):
                    self.X[0] = self.X[2]
                else: self.H /= self.d
            else:
                if self.f(self.X[1]) < self.f(self.X[0]):
                    self.X[0] = self.X[1]
                else: self.H /= self.d
            #условие окончания
            Ostanov = True
            for i in self.H:
                if i  > self.e: Ostanov = False
            k += 1

        self.result = self.X[1]
        print(k)





if __name__ == '__main__':
    from main import f

    n = 2
    h = 0.2
    d = 2
    m = 0.5
    e = 0.1
    my_HukJavis = HukJivs(n, h, d, m, e, f)
    my_HukJavis.eval()

    print(my_HukJavis.result, f(my_HukJavis.result))