from numpy import identity,array,dot,zeros,argmax
import math
from casadi import *

EPSILON = 10**(-6)

def powellMethod(F,x,h=0.1):
    
    def f(lmbd): return F(x + lmbd*v)    # funkcja F dla kierunku ksi

    n = len(x)                           # ilość zmiennych w funkcji
    ksi = identity(n)                    # baza wejsciowa utworzona z wzajemnie ortogonalnych vektorów
    for j in range(30):                  # max 30 cykli
        xOld = x.copy()                  # przypisanie punktu startowego 
        fOld = F(xOld)

      # Dla i = 1,2,...,n następuje obliczanie lambda minimalizujące 
      # oraz współrzedne nowego punktu x
        for i in range(n):
            v = ksi[i]
            a,b = Interval4GoldenRatio(f,0.0,h)
            lmbd,fMin = GoldenRatio(f,a,b)
            fOld = fMin
            x = x + lmbd*v

      # wyznaczanie składowych kierunku sprzężonego    
        v = xOld - x
      # wyznaczenie lambda minimalizujące wzdłuż nowego kierunku v 
      # oraz współżedne nowego punktu startowego
        a,b = Interval4GoldenRatio(f,0.0,h)
        lmbd,fLast = GoldenRatio(f,a,b)
        x = x + lmbd*v
    
      # sprawdzanie czy jest spełnione kryterium dla minimum
        if sqrt(dot(x-xOld,x-xOld)/n) < EPSILON: return x,j+1

      # modyfikacja kierunków poszukiwań
        for i in range(n-1):
            ksi[i] = ksi[i+1]
        ksi[n-1] = v

    print ("Powell did not converge")    

# określenie zakresów dla złotego podziału
def Interval4GoldenRatio(f,x1,h):
    c = 1.618033989 
    f1 = f(x1)
    x2 = x1 + h; f2 = f(x2)
  # określenie kierunku spadku
  # zmiana znaku przy h  jeśli konieczna
    if f2 > f1:
        h = -h
        x2 = x1 + h; f2 = f(x2)
      # sprawdzenie czy minimum znajduje się między x1 - h  a x1 + h
        if f2 > f1: return x2,x1 - h 
  # przeszukanie pętli max 100 cykli
    for i in range (100):    
        h = c*h
        x3 = x2 + h; f3 = f(x3)
        if f3 > f2: return x1,x3
        x1 = x2; x2 = x3
        f1 = f2; f2 = f3
    print("Bracket did not find a mimimum")

# metoda złotego podziału
def GoldenRatio(f,a,b):
    k = ( sqrt( 5 ) - 1 ) / 2
    xL = b - k * ( b - a )
    xR = a + k * ( b - a )
    f1 = f(xL) 
    f2 = f(xR)

    while ( ( b - a ) > EPSILON ):
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

    if f1 < f2: f = f1
    else: f = f2

    return (a+b)/2, f


#definicja funkcji
def F(x):       

    #F = x[0]**2 + x[0]*x[1] + 2 * x[0] + x[1]**2
    #F = (1.5 - x[0] + x[0]*x[1])**2 + (2.25 - x[0] + x[0]*x[1]**2)**2 + (2.625 - x[0] + x[0]*x[1]**3)**2
    #F = (x[0] + 2*x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2
    #F = 0.26 * (x[0]**2 + x[1]**2) - 0.48 * x[0] * x[1]
    F = 100 * sqrt(fabs(x[1]-0.01*x[0]**2)) + 0.01*fabs(x[0] + 10)
    #F = (1 + (x[0] + x[1] + 1)**2 * (19 - 14 * x[0] + 3 * x[0]**2 - 14 * x[1] + 6 * x[0] * x[1] + 3 * x[1]**2)) *  (30 + (2 * x[0] - 3 * x[1])**2 * (18 - 32 * x[0] + 12 * x[0]**2 + 48 * x[1] - 36 * x[0] * x[1] + 27 * x[1]**2))

    return F 

if __name__ == '__main__':
    startingPoint_array = list()
    
    startingPointMatrix = input("Enter how many elements does the starting point has: ")
    #dla funckji F(x,y) wpisać 2, dla funkcji F(x,y,z) wpisać 3 itp.
    x0 = zeros(int(startingPointMatrix))                  
    minimumPoint = zeros(int(startingPointMatrix))

    print ('Enter coordinates of the starting point: ')
    for i in range(int(startingPointMatrix)):
        x0[i] = int(input("Insert grid coordinate : "))
        #kolejno podawane koordynaty punktu x[0] = x x[1] = y --> (x,y)

    minimumPoint = powellMethod(F, x0, h=0.1)
    minimalizedFunction = F(minimumPoint[0])
    print("Minimum -> ", minimumPoint[0])
    print("F(minimum) = :", minimalizedFunction)
    
