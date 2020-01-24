import numpy as np
from math import *

class gradPermStep(object):
    def __init__(self, n, h, e, f):
        self.f = f
        self.result = np.array([]*n)
        self.n = n
        self.e = e
        self.h = h
        self.X = np.array([0.0] * 3 * n).reshape(3, n)
        self.X[0] = np.array([0.0]*n)
        self.grad = np.array([0.0]*n)

    def eval(self):
        Ostanov = False
        k = 0
        while not Ostanov:

            #непрерывна ли функция в этой точке
            try:
                f = self.f(self.X[0])
            except Exception as err:
                print(err)
                break

            #градиент
            del_x = 0.0001
            for i in range(self.n):
                self.X[2] = self.X[0]
                self.X[2,i] = self.X[2,i] + del_x
                self.grad[i] = (self.f(self.X[2]) - f) / del_x

            # шаг
            self.X[1] = self.X[0] - self.h * self.grad
            #уменьшение шага, пока не будет уменьшение функции
            while not (self.f(self.X[1]) < self.f(self.X[0])):
                self.h /= 2
                self.X[1] = self.X[0] - self.h*self.grad

            k += 1
            self.X[0] = self.X[1]
            #новый градиент
            for i in range(self.n):
                self.X[2] = self.X[0]
                self.X[2,i] = self.X[2,i] + del_x
                self.grad[i] = (self.f(self.X[2]) - f) / del_x

            #остановка?
            res = 0
            for i in self.grad:
                res += i*i
            Ostanov = sqrt(res) < self.e

        self.result = self.X[0]
        print(k)


if __name__ == '__main__':
    from main import f

    n = 2
    h = 0.4
    e = 0.1
    my_gradPermStep = gradPermStep(n, h, e, f)
    my_gradPermStep.eval()
    print('res: ', my_gradPermStep.result, f(my_gradPermStep.result))