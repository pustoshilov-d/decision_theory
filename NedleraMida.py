from math import *
import numpy as np
class NedleraMid:
    def compress(self, n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f):
        # сжатие
        x_mirrowed = x_center + y * (self.X[k_x_high] - x_center)

        # 10
        if f(x_mirrowed) < f(self.X[k_x_high]):
            # сжатие успешно
            self.X[k_x_high] = x_mirrowed
        else:
            self.reduce(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)

    def expand(self, n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f):
        # растяжение
        x_mirrowed = x_center + b * (self.X[k_x_high] - x_center)

        # 8
        if f(x_mirrowed) > f(self.X[k_x_high]):
            # растяжение успешно
            self.X[k_x_high] = x_mirrowed
        else:
            # 9
            if (F_low < f(x_mirrowed) and f(x_mirrowed) < F_high):
                self.compress(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)
            else:
                self.reduce(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)

    def reduce(self, n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f):
        # 11 редукция
        F_res = np.array([0.0] * n_1_axis)
        for i in range(n_1_axis):
            F_res[i] = f(self.X[i])

        r_x_min = np.argmin(F_res)
        for i in range(n):
            if i != r_x_min:
                self.X[i] = self.X[r_x_min] + 0.5 * (self.X[i] - self.X[r_x_min])



    def eval(self, f,n,m,e,b,y):
        # init
        Ostanov = False
#        X0 = np.array([0.0] * n)
        X0 = np.array([-0.64, -2.26])
        n_1_axis = n
        n += 1
        self.X = np.array([0.0] * n_1_axis * n).reshape(n, n_1_axis)

        # заполнение числами
        d1 = m * (sqrt(n_1_axis + 1) - 1) / (n_1_axis * sqrt(2))
        d2 = m * (sqrt(n_1_axis + 1) + n_1_axis - 1) / (n_1_axis * sqrt(2))

        k=0

        self.X[0] = X0
        for i in range(1, n):
            for j in range(n_1_axis):
                if (j + 1 == i):
                    self.X[i][j] = self.X[0][j] + d1
                else:
                    self.X[i][j] = self.X[0][j] + d2

        #Цикл до условия остановки
        while not Ostanov:
            #индекс максимального значени f
            F_res = np.array([0.0]*n)
            for i in range(n):
                F_res[i] = f(self.X[i])
            k_x_high = np.argmax(F_res)
            F_high = F_res[k_x_high]

            k_x_low = np.argmin(F_res)
            F_low = F_res[k_x_low]

            k_x_sec = np.argmax(np.delete(F_res,k_x_high,0))
            F_sec = F_res[k_x_sec]

            #центр тяжести
            x_center = np.array([0.0]*n_1_axis)
            for i in range(n):
                if i != k_x_high:
                    x_center += self.X[i]
            x_center /= n - 1

            #отражение
            x_mirrowed = 2 * x_center - self.X[k_x_high]
            #6
            if f(x_mirrowed) < f(self.X[k_x_high]):
                #успешно отражение
                self.X[k_x_high] = x_mirrowed

                #7
                if f(self.X[k_x_high]) < F_low:
                    self.expand(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)
                else:
                    #9
                    if (F_low < f(x_mirrowed) and f(x_mirrowed) < F_high):
                        self.compress(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)
                    else:
                        self.reduce(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)
            # 9
            else:
                self.compress(n_1_axis, x_mirrowed, F_low, F_high, x_center, k_x_high, y, b, n, f)


            #центр тяжести симлекса
            x_center = np.array([0.0]*n_1_axis)
            for i in range(n):
                x_center += self.X[i]
            x_center /= n
            #критерий останова

            sum = 0
            for i in range(n):
                sum += pow(f(self.X[i]) - f(x_center),2)

            a = sqrt(sum/(n))
            Ostanov = a < e
            k+=1

        #вывод мин решения
        F_res = np.array([0.0]*n_1_axis)
        for i in range(n_1_axis):
            F_res[i] = f(self.X[i])
        k_x_min = np.argmax(F_res)
        print(k)
        return(self.X[k_x_min])


def NedleraMida(f,n,m,e,b,y):
    nedleraMida = NedleraMid()
    return nedleraMida.eval(f,n,m,e,b,y)


if __name__ == '__main__':
    from main import f
    n = 2
    m = 1.0
    e = 0.1
    b = 2.8
    y = 0.4

    print(NedleraMida(f,n,m,e,b,y), f(NedleraMida(f,n,m,e,b,y)))