import numpy as np
from math import *

# [0.54326069 0.09303254] -0.2727042740156461
class gradPoKoor(object):
    def __init__(self, n, e, f):
        self.f = f
        self.result = np.array([]*n)
        self.n = n
        self.e = e
        self.X = np.array([0.0] * n)
        self.grad = np.array([0.0]*n)
        self.Gesse = np.array([0.0]*n*n).reshape(n,n)
        self.del_x = 0.0001
        self.E = np.array([0.0]*n)

    def init_e_vec(self, i):
        self.E = np.array([0.0] * self.n*self.n).reshape(self.n,self.n)
        self.E[i,i] = 1.0


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

            for i in range(self.n):

                #единичный вектор
                self.init_e_vec(i)
                #градиент
                self.evalGrad()
                #матрица Гессе
                self.evalGesse()

                try:
                    self.h = np.dot(self.grad, self.grad) / np.dot(np.dot(self.Gesse, self.grad), self.grad)
                except Exception as e: self.h = 1
                if abs(self.h) == inf: self.h = 1

                self.X += - self.h * np.dot(self.grad, self.E)

                #остановка?
            res = 0
            self.evalGrad()
            for i in self.grad:
                res += i*i
            Ostanov = sqrt(res) < self.e
            k += 1
        self.result = self.X
        print(k)

if __name__ == '__main__':
    from main import f

    n = 2
    e = 0.1
    my_gradPoKoor = gradPoKoor(n, e, f)
    my_gradPoKoor.eval()
    print('res: ', my_gradPoKoor.result, f(my_gradPoKoor.result))