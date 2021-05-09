from casadi import *

x1 = SX.sym('x1')
x2 = SX.sym('x2')
x3 = SX.sym('x3')
x4 = SX.sym('x4')
x5 = SX.sym('x5')



def GoldenRatioMethod(a, b, equalsss):
    d = SX.sym('d')
    func = Function('func', [d], [eval(equalsss)])
    k = (sqrt(5) - 1) / 2

    xL = b - k * (b - a)
    xR = a + k * (b - a)

    EPSILON = 10**(-6)

    while (b - a) > EPSILON:
        if func(xL) < func(xR):
            b = xR
            xR = xL
            xL = b - k * (b - a)
        else:
            a = xL
            xL = xR
            xR = a + k * (b - a)


    return (a+b)/2


if __name__ == '__main__':

    x = SX.sym('x')
    a = int(input("Set a: "))
    b = int(input("Set b: "))

    expression = input("Set expression: ")

    r = GoldenRatioMethod(a, b, expression)
    print(r)

    # n = int(input("Set number of variables: "))
    #
    # X = [0] * 5
    #
    # expression = input("Set expression: ")
    # f = Function('f', [x1, x2, x3, x4, x5], [eval(expression)])
    #
    # for i in range(n):
    #     tempx = input("Set variable")
    #     X[i] = float(tempx)
    #
    # print(f(X[0], X[1], X[2], X[3], X[4]))


