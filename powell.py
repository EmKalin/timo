from PySide6.QtCore import Signal, QObject
from numpy import identity, array, dot, zeros, argmax
import math
from casadi import *
import parser
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtCore import Signal


class PowellInstance(QObject):
    speak = Signal(dict)

    def __init__(self, parent):
        self.parent = parent
        super(PowellInstance, self).__init__()
        self.speak.connect(self.parent.tempSlot)

    def powellMethodA(self, set_function, x, L, epsilon, h=0.1):
        def f(lmbd):
            x_lamb = x + lmbd * v
            for i in range(1, len(x_lamb) + 1):
                locals()['x%s' % i] = x_lamb[i - 1]  # funkcja F dla kierunku ksi
            result = eval(set_function)
            for i in range(1, len(x) + 1):
                locals()['x%s' % i] = x[i - 1]
            return result

        n = len(x)  # ilość zmiennych w funkcji
        ksi = identity(n)  # baza wejsciowa utworzona z wzajemnie ortogonalnych vektorów
        for j in range(L):  # max 30 cykli
            xOld = x.copy()  # przypisanie punktu startowego
            for i in range(1, len(x) + 1):
                locals()['x%s' % i] = xOld[i - 1]
            fOld = eval(set_function)

            # Dla i = 1,2,...,n następuje obliczanie lambda minimalizujące
            # oraz współrzedne nowego punktu x
            for i in range(n):
                v = ksi[i]
                a, b = self.Interval4GoldenRatio(f, 0.0, h)
                lmbd, fMin = self.GoldenRatio(f, a, b, epsilon)
                fOld = fMin
                x = x + lmbd * v


            # wyznaczanie składowych kierunku sprzężonego
            v = xOld - x
            # wyznaczenie lambda minimalizujące wzdłuż nowego kierunku v
            # oraz współżedne nowego punktu startowego
            a, b = self.Interval4GoldenRatio(f, 0.0, h)
            lmbd, fLast = self.GoldenRatio(f, a, b, epsilon)
            x = x + lmbd * v

            xIt = x.copy()  # przypisanie punktu startowego
            for i in range(1, len(x) + 1):
                locals()['x%s' % i] = xIt[i - 1]
            fIt = eval(set_function)


            kryteriumStopu = sqrt(dot(x - xOld, x - xOld) / n)
            dataExport = {"x": x, "stop": kryteriumStopu, "fmin": fIt}
            self.speak.emit(dataExport)

            # sprawdzanie czy jest spełnione kryterium dla minimum
            if kryteriumStopu < epsilon:
                return x, kryteriumStopu, j + 1

            # modyfikacja kierunków poszukiwań
            for i in range(n - 1):
                ksi[i] = ksi[i + 1]
            ksi[n - 1] = v

        print("Powell did not converge")


    def powellMethodB(self, set_function, x, L, epsilon, a, b, h=0.1):
        def f(lmbd):
            x_lamb = x + lmbd * v
            for i in range(1, len(x_lamb) + 1):
                locals()['x%s' % i] = x_lamb[i - 1]  # funkcja F dla kierunku ksi
            result = eval(set_function)
            for i in range(1, len(x) + 1):
                locals()['x%s' % i] = x[i - 1]
            return result

        n = len(x)  # ilość zmiennych w funkcji
        ksi = identity(n)  # baza wejsciowa utworzona z wzajemnie ortogonalnych vektorów
        for j in range(L):  # max 30 cykli
            xOld = x.copy()  # przypisanie punktu startowego
            for i in range(1, len(x) + 1):
                locals()['x%s' % i] = xOld[i - 1]
            fOld = eval(set_function)

            # Dla i = 1,2,...,n następuje obliczanie lambda minimalizujące
            # oraz współrzedne nowego punktu x
            for i in range(n):
                v = ksi[i]
                # a,b = Interval4GoldenRatio(f,0.0,h)
                lmbd, fMin = self.GoldenRatio(f, a, b, epsilon)
                fOld = fMin
                x = x + lmbd * v

            # wyznaczanie składowych kierunku sprzężonego
            v = xOld - x
            # wyznaczenie lambda minimalizujące wzdłuż nowego kierunku v
            # oraz współżedne nowego punktu startowego
            # a,b = Interval4GoldenRatio(f,0.0,h)
            lmbd, fLast = self.GoldenRatio(f, a, b, epsilon)
            x = x + lmbd * v

            xIt = x.copy()  # przypisanie punktu startowego
            for i in range(1, len(x) + 1):
                locals()['x%s' % i] = xIt[i - 1]
            fIt = eval(set_function)

            kryteriumStopu = sqrt(dot(x - xOld, x - xOld) / n)
            dataExport = {"x": x, "stop": kryteriumStopu, "fmin": fIt}
            self.speak.emit(dataExport)

            # sprawdzanie czy jest spełnione kryterium dla minimum
            if kryteriumStopu < epsilon:
                return x, kryteriumStopu, j + 1

            # modyfikacja kierunków poszukiwań
            for i in range(n - 1):
                ksi[i] = ksi[i + 1]
            ksi[n - 1] = v

        print("Powell did not converge")

    @staticmethod
    # określenie zakresów dla złotego podziału
    def Interval4GoldenRatio(f, xL, h):
        c = 1.618033989
        f1 = f(xL)
        xR = xL + h;
        f2 = f(xR)
        # określenie kierunku spadku
        # zmiana znaku przy h  jeśli konieczna
        if f2 > f1:
            h = -h
            xR = xL + h;
            f2 = f(xR)
            # sprawdzenie czy minimum znajduje się między xL - h  a xL + h
            if f2 > f1: return xR, xL - h
            # przeszukanie pętli max 100 cykli
        for i in range(100):
            h = c * h
            x3 = xR + h;
            f3 = f(x3)
            if f3 > f2: return xL, x3
            xL = xR;
            xR = x3
            f1 = f2;
            f2 = f3
        print("Bracket did not find a mimimum")

    @staticmethod
    # metoda złotego podziału
    def GoldenRatio(f, a, b, epsilon):
        k = (sqrt(5) - 1) / 2
        xL = b - k * (b - a)
        xR = a + k * (b - a)
        f1 = f(xL)
        f2 = f(xR)

        while ((b - a) > epsilon):
            if f1 < f2:
                b = xR
                xR = xL
                xL = b - k * (b - a)
                f2 = f1
                f1 = f(xL)
            else:
                a = xL
                xL = xR
                xR = a + k * (b - a)
                f1 = f2
                f2 = f(xR)

        if f1 < f2:
            f = f1
        else:
            f = f2

        return (a + b) / 2, f

    @staticmethod
    def plot(set_function, x0, L, a, b, minPoint):
        x = np.linspace(a, b, L)
        y = np.linspace(a, b, L)
        X, Y = np.meshgrid(x, y)
        funkcja = set_function
        funkcja = funkcja.replace("x1", "X")
        funkcja = funkcja.replace("x2", "Y")
        Z = eval(funkcja)

        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(X, Y, Z)
        fig.colorbar(cp)  # Add a colorbar to a plot
        ax.set_title('Filled Contours Plot')
        ax.set_xlabel('x (cm)')
        ax.set_ylabel('y (cm)')

        # plot(x0[0], x0[1], 'po')
        # plot(minPoint[0], minPoint[1], 'ro')

        plt.show()


# if __name__ == '__main__':
#     # Przeniesione
#     #set_x0 = str(input('Enter the starting point: '))
#     #x0 = [float(x) for x in set_x0.split(',')]
#
#     #L = int(input('Enter number of iterations: '))
#
#     #estimation = input('Enter tolerance: ')
#     #epsilon = eval(estimation.replace("^", "**"))
#
#     # print("How to you want to choose [a,b]?")
#     # print("To use the Swan method, enter 1.")
#     # print("to enter them yourself, enter 2.")
#     # caseVariable = int(input("Answer: "))
#
#     # if caseVariable == 1:
#         # formula = str(input('Enter function: '))
#         # set_formula = formula.replace("^", "**")
#         # set_function = parser.expr(set_formula).compile()
#
#         # minimumPoint = powellMethodA(set_function, x0, L, epsilon, h=0.1)
#     # elif caseVariable == 2:
#         ab_tab = str(input('Enter brackets for Golden Ratio search: '))
#         a = float(ab_tab.split(',')[0])
#         b = float(ab_tab.split(',')[1])
#
#         formula = str(input('Enter function: '))
#         set_formula = formula.replace("^", "**")
#         set_function = parser.expr(set_formula).compile()
#
#         minimumPoint = powellMethodB(set_function, x0, L, epsilon, a, b, h=0.1)
#     else:
#         print("Invalid argument.")
#
#     for i in range(1, len(minimumPoint[0]) + 1):
#         locals()['x%s' % i] = minimumPoint[0][i - 1]
#     minimalizedFunction = eval(set_function)
#
#     minimumPoint[0]
#     print("Minimum -> ", minimumPoint)
#     print("F(minimum) = :", minimalizedFunction)
#
#     # plot(set_formula, x0, L, a, b, minimumPoint[0])
#
#     del formula
#     del set_formula