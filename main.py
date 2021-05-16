from numpy import identity,array,dot,zeros,argmax
import math
from casadi import *

EPSILON = 10**(-6)

def powellMethod(F,x,h=0.1):
    def f(d): return F(x + d*e)    # F in direction of e

    n = len(x)                     # Number of design variables
    df = zeros(n)                  # Decreases of F stored here
    u = identity(n)                # Vectors v stored here by rows
    for j in range(30):            # Allow for 30 cycles:
        xOld = x.copy()            # Save starting point
        fOld = F(xOld)
      # First n line searches record decreases of F
        for i in range(n):
            e = u[i]
            a,b = bracket(f,0.0,h)
            d,fMin = GoldenRatio(f,a,b)
            df[i] = fOld - fMin
            fOld = fMin
            x = x + d*e
      # Last line search in the cycle    
        e = x - xOld
        a,b = bracket(f,0.0,h)
        d,fLast = GoldenRatio(f,a,b)
        x = x + d*e
      # Check for convergence
        if sqrt(dot(x-xOld,x-xOld)/n) < EPSILON: 
            return x,j+1
      # Identify biggest decrease & update search directions
        iMax = argmax(df)
        for i in range(iMax,n-1):
            u[i] = u[i+1]
        u[n-1] = e
    print ("Powell did not converge")    


def bracket(f,x1,h):
    c = 1.618033989 
    f1 = f(x1)
    x2 = x1 + h
    f2 = f(x2)
  # Determine downhill direction and change sign of h if needed
    if f2 > f1:
        h = -h
        x2 = x1 + h
        f2 = f(x2)
      # Check if minimum between x1 - h and x1 + h
        if f2 > f1: 
            return x2,x1 - h 
  # Search loop
    for i in range (100):    
        h = c*h
        x3 = x2 + h; f3 = f(x3)
        if f3 > f2: 
            return x1,x3
        x1 = x2
        x2 = x3
        f1 = f2
        f2 = f3
    print("Bracket did not find a mimimum")

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
def F(x):       # Definicja funkcji    
    #F = 100 * sqrt(abs(x[1] - 0.01*x[0]**2)) + 0.01 * abs(x[0] + 10)
    F = (x[0] + 2 * x[1] - 7)**2 + (2*x[0] + x[1] - 5)**2
    #F = 0.26 * (x[0]**2 + x[1]**2) - 0.48 * x[0] * x[1]
    #F = 100*(x[1]-x[0]**2)**2 + (1 - x[0])**2

    #F = x[0]**4 - 3*x[0]**2 * x[1]**2 + (2/3) * x[0]**3 + 3*x[1]**2 - 2
    #F = 3*x[0]**4 - (2/3)*x[1]**3 + 2*x[0]**2*x[1] - 2*x[0]**2 + x[1]**2
    #F = x[0]**2 + x[0]*x[1] + 2 * x[0] + x[1]**2
    return F

if __name__ == '__main__':
    startingPoint_array = list()
    startingPointMatrix = input("Enter how many elements does the starting point has: ")
    x0 = zeros(int(startingPointMatrix))                  #starting point z = (x,y)
    minimumPoint = zeros(int(startingPointMatrix))

    print ('Enter coordinates of the starting point: ')
    for i in range(int(startingPointMatrix)):
        x0[i] = int(input("Insert grid coordinate : "))

    minimumPoint = powellMethod(F, x0, h=0.1)
    minimalizedFunction = F(minimumPoint[0])
    print("Minimum -> ", minimumPoint)
    print("F(minimum) = :", minimalizedFunction)
    
