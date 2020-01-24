from math import *
import numpy as np

def Simplecs(f,n,m, e):

    #init
    Ostanov = False
    X0 = np.array([-0.58,-2.17])
    n_1_axis = n
    n += 1
    X = np.array([0.0]*n_1_axis*n).reshape(n,n_1_axis)

    #заполнение числами
    d1 = m * (sqrt(n_1_axis + 1) - 1) / (n_1_axis * sqrt(2))
    d2 = m * (sqrt(n_1_axis + 1) + n_1_axis - 1) / (n_1_axis * sqrt(2))

    k = 0
    X[0] = X0
    for i in range(1,n):
        for j in range(n_1_axis):
            if (j+1==i):
                X[i][j] = X[0][j] + d1
            else:
                X[i][j] = X[0][j] + d2


    #Цикл до условия остановки
    while not Ostanov:
        #индекс максимального значени f
        F_res = np.array([0.0]*n)
        for i in range(n):
            F_res[i] = f(X[i])
        k_x_max = np.argmax(F_res)

        #центр тяжести
        x_center = np.array([0.0]*n_1_axis)
        for i in range(n):
            if i != k_x_max:
                x_center += X[i]
        x_center /= n -1

        #отражение
        x_mirrowed = 2 * x_center - X[k_x_max]
        if f(x_mirrowed) < f(X[k_x_max]):
            X[k_x_max] = x_mirrowed
        else:
            #редукция
            r_x_min = np.argmin(F_res)
            for i in range(n):
                if i !=r_x_min:
                    X[i] = X[r_x_min] + 0.5*(X[i] - X[r_x_min])

        #центр тяжести симлекса
        x_center = np.array([0.0]*n_1_axis)
        for i in range(n):
                x_center += X[i]
        x_center /= n

        Ostanov = True
        #условие останова
        for i in range(n):
            if abs(f(X[i])-f(x_center)) >= e: Ostanov = False
        k += 1

    #вывод мин решения
    F_res = np.array([0.0]*n)
    for i in range(n):
        F_res[i] = f(X[i])
    k_x_min = np.argmax(F_res)
    print(k)


    return(X[k_x_min])

if __name__ == '__main__':
    from main import f
    n = 2
    m = 0.25
    e = 0.1
    x = Simplecs(f,n,m,e)
    print(x,f(x))