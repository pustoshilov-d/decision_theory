from HukJivs import HukJivs
from Simplecs import Simplecs
from NedleraMida import NedleraMida
from gradPermStep import gradPermStep
from gradFastStep import gradFastStep
from gradPoKoor import gradPoKoor
from Fletcher import Fletcher
from Nutona import Nutona
from NutonRafson import NutonRafson
import time
import matplotlib.pyplot as pylab
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np



def f(X):
# return X[0]*X[0] + X[0]*X[1] + 3*X[1]*X[1] - X[0]
    return X[0]*X[0] - X[0]*X[1] + 3*X[1]*X[1] - X[0] + 13*X[1] + 3

def makeChoice(choise):
    n = 2
    e = 0.01

    if int(choise) == 0:
        if n == 2:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            X = np.arange(-5, 5, 0.25)
            Y = np.arange(-5, 5, 0.25)
            Z = np.array([0.0]*len(X)*len(X)).reshape(len(X),len(X))
            for i in range(len(X)):
                for j in range(len(Y)):
                    Z[i,j] = f(np.array([X[i],Y[j]]))
            X, Y = np.meshgrid(X, Y)
            surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                                   linewidth=0, antialiased=False)
            plt.show()


        time_mass = np.array([0.0] * 9)
        try:
            for i in range(9):
                begin_time = time.time()
                makeChoice(i+1)
                time_mass[i] = time.time()-begin_time
                print('Time: ', time_mass[i])
        except Exception as err: pass

        pylab.plot(range(1,10), time_mass)
        pylab.show()


    if int(choise) == 1:
        m = 0.25
        print('1. Симплекс: X[] = ',Simplecs(f,n,m,e),', Y =', f(Simplecs(f,n,m,e)))

    if int(choise) == 2:
        m = 0.05
        b = 2.8
        y = 0.4
        print('2. Нелдера-Мида: X[] = ',NedleraMida(f,n,m,e,b,y),', Y =', f(NedleraMida(f,n,m,e,b,y)))

    if int(choise) == 3:
        h = 0.2
        d = 2
        m = 0.5
        my_HukJavis = HukJivs(n, h, d, m, e, f)
        my_HukJavis.eval()
        print('3. Хук-Дживис: X[] = ',my_HukJavis.result,', Y =', f(my_HukJavis.result))

    if int(choise) == 4:
        h = 0.4
        my_gradPermStep = gradPermStep(n, h, e, f)
        my_gradPermStep.eval()
        print('4. Градиентного с постоянным шагом: X[] = ',my_gradPermStep.result,', Y =', f(my_gradPermStep.result))

    if int(choise) == 5:
        my_gradFastStep = gradFastStep(n, e, f)
        my_gradFastStep.eval()
        print('5. Градиент наискорейшего спуска: X[] = ',my_gradFastStep.result,', Y =', f(my_gradFastStep.result))

    if int(choise) == 6:
        my_gradPoKoor = gradPoKoor(n, e, f)
        my_gradPoKoor.eval()
        print('6. Градиент пкоординатного спуска: X[] = ',my_gradPoKoor.result,', Y =', f(my_gradPoKoor.result))

    if int(choise) == 7:
        n = 2
        e = 0.0001
        my_Fletcher = Fletcher(n, e, f)
        my_Fletcher.eval()
        print('7. Фетчера: X[] = ',my_Fletcher.result,', Y =', f(my_Fletcher.result))

    if int(choise) == 8:
        my_Nutona = Nutona(n, e, f)
        my_Nutona.eval()
        print('8. Ньютона: X[] = ',my_Nutona.result,', Y =', f(my_Nutona.result))

    if int(choise) == 9:
        my_NutonRafson = NutonRafson(n, e, f)
        my_NutonRafson.eval()
        print('9. Ньютона-Рафсона: X[] = ',my_NutonRafson.result,', Y =', f(my_NutonRafson.result))

if __name__ == '__main__':
    while True:
        print('\n0.Все\n'
              '1. Симплекс\n'
              '2. Нелдера-Мида\n'
              '3. Хук-Дживис\n'
              '4. Градиентного с постоянным шагом\n'
               '5. Градиент наискорейшего спуска\n'
                '6. Градиент пкоординатного спуска\n'
                '7. Фетчера\n'
                '8. Ньютона\n'
                '9. Ньютона-Рафсона')
        choise = input('Выберите номер метода: ')
        makeChoice(choise)



