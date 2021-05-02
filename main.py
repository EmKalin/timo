from casadi import *

x1 = SX.sym('x1')
x2 = SX.sym('x2')
x3 = SX.sym('x3')
x4 = SX.sym('x4')
x5 = SX.sym('x5')


if __name__ == '__main__':
    n = int(input("Set number of variables: "))

    X = [0] * 5

    expression = input("Set expression: ")
    f = Function('f', [x1, x2, x3, x4, x5], [eval(expression)])

    for i in range(n):
        tempx = input("Set variable")
        X[i] = float(tempx)

    print(f(X[0], X[1], X[2], X[3], X[4]))
