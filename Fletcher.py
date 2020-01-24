import numpy as np
from math import *

# [0.54326069 0.09303254] -0.2727042740156461
class Fletcher(object):
    def __init__(self, n, e, f):
        self.f = f
        self.result = np.array([]*n)
        self.n = n
        self.e = e
        self.X = np.array([0.0] * n)
        self.grad = np.array([0.0]*n)
        self.Gesse = np.array([0.0]*n*n).reshape(n,n)
        self.del_x = 0.000001
        self.P = np.array([0.0]*n*2).reshape(2,n)
        self.b = 0
        self.gradNorm = 0

    def evalGradNorm(self):
        res = 0
        for i in self.grad:
            res += i * i
        return res


    def evalP(self):
        self.evalGrad()
        self.b = self.evalGradNorm()/self.gradNorm
        self.P[0] = self.grad + self.b * self.P[1]

    def change(self, i, del_x, j = None):
        mass = np.array(self.X)
        mass[i] += del_x
        if j != None:
            mass[j] += del_x
        return mass

    def evalGrad(self):
        for i in range(self.n):
            X_changed = self.change(i, self.del_x)
            self.grad[i] = (self.f(X_changed) - self.f(self.X)) / self.del_x

    def evalGesse(self):
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    u1 = self.f(self.change(i, self.del_x))
                    u2 = self.f(self.X)
                    u3 = self.f(self.change(i, -self.del_x))
                    self.Gesse[i,j] = (u1-2*u2+u3) / (self.del_x * self.del_x)

                else:
                    u1 = self.f(self.X)
                    u2 = self.f(self.change(i, -self.del_x))
                    u3 = self.f(self.change(j, -self.del_x))
                    u4 = self.f(self.change(i, -self.del_x, j))
                    self.Gesse[i, j] = (u1 - u2 - u3 + u4) / (self.del_x * self.del_x)


    def eval(self):
        Ostanov = False
        k = 0
        while not Ostanov:

            #непрерывна ли функция в этой точке
            try:
                f = self.f(self.X)
            except Exception as err:
                print(err)
                break

            #градиент
            self.evalGrad()
            #верктор спуска
            if k == 0:
                self.P[0] = - self.grad
            else:
                self.evalP()
            self.gradNorm = self.evalGradNorm()

            #матрица Гессе
            self.evalGesse()

            try:
                self.h = np.dot(self.grad, self.P[0]) / np.dot(np.dot(self.Gesse, self.P[0]), self.P[0])
            except Exception as e: self.h = 1
            if abs(self.h) == inf: self.h = 1

            self.X += - self.h * self.P[0]

            #остановка?
            self.evalGrad()
            Ostanov = sqrt(self.evalGradNorm()) < self.e
            self.P[1] = self.P[0]
            k += 1

        self.result = self.X
        print(k)

if __name__ == '__main__':
    from main import f

    n = 2
    e = 0.1
    my_Fletcher = Fletcher(n, e, f)
    my_Fletcher.eval()
    print('res: ', my_Fletcher.result, f(my_Fletcher.result))