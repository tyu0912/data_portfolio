import numpy as np
from scipy.optimize import minimize

C = open('C.txt','r').read().splitlines()
W = open('W.txt','r').read().splitlines()
D = open('D.txt','r').read().splitlines()
G = open('G.txt','r').read().splitlines()

def splitdata(file):
    for index,line in enumerate(file):
        file[index] = line.split('\t')
    
    return(file)

def objective(x, sign=-1.0):

    x = list(map(int, x))
    pos = 3

    Cvalue = float(C[x[0]][pos]) + float(C[x[1]][pos])

    Wvalue = float(W[x[2]][pos]) + float(W[x[3]][pos]) + float(W[x[4]][pos])

    Dvalue = float(D[x[5]][pos]) + float(D[x[6]][pos])

    Gvalue = float(G[x[7]][pos])

    Uvalue = float(U[x[8]][pos])

    grand_value = sign*(Cvalue + Wvalue + Dvalue + Gvalue + Uvalue)

    #print(grand_value)
    return grand_value

def constraint_cost(x):
    
    x = list(map(int, x))
    pos = 6

    Ccost = int(C[x[0]][pos]) + int(C[x[1]][pos])

    Wcost = int(W[x[2]][pos]) + int(W[x[3]][pos]) + int(W[x[4]][pos])

    Dcost = int(D[x[5]][pos]) + int(D[x[6]][pos])

    Gcost = int(G[x[7]][pos])

    Ucost = int(U[x[8]][pos])

    grand_cost =  50000 - (Ccost + Wcost + Dcost + Gcost + Ucost)

    #print(grand_cost)
    return grand_cost

def constraint_C(x):
    if x[0] == x[1] and x[0]:
        return 0
    else: 
        return 1 

def constraint_W(x):
    if x[2] == x[3] or x[2] == x[4] or x[3] == x[4]:
        return 0
    else: 
        return 1 

def constraint_D(x):
    if x[5] == init[6]:
        return 0
    else: 
        return 1

con1 = {'type':'ineq','fun':constraint_cost}
con2 = {'type':'ineq','fun':constraint_C}
con3 = {'type':'ineq','fun':constraint_W}
con4 = {'type':'ineq','fun':constraint_D}

con = [con1, con2, con3, con4]

c0 = [0,1]
w0 = [0,1,2]
d0 = [0,1]
g0 = [0]
u0 = [0]
init = c0+w0+d0+g0+u0

C = splitdata(C)
W = splitdata(W)
D = splitdata(D)
G = splitdata(G)
U = C + W + D + G

sol = minimize(objective, init, method='COBYLA',constraints=con)

print(sol)



