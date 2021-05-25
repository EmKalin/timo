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
    err = Signal(str)

    def __init__(self, parent):
        self.parent = parent
        super(PowellInstance, self).__init__()
        self.speak.connect(self.parent.tempSlot)
        self.err.connect(self.parent.tempSlot)


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
            # oraz współrzedne nowego punktu startowego
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

        self.err.emit("Powell did not converge")





    @staticmethod
    # METODA ZŁOTEGO PODZIAŁU
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



