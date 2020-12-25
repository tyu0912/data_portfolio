import pulp as p
import itertools as i

C = open('C.txt','r').read().splitlines()
W = open('W.txt','r').read().splitlines()
D = open('D.txt','r').read().splitlines()
G = open('G.txt','r').read().splitlines()

def splitdata(file):
    for index,line in enumerate(file):
        file[index] = line.split('\t')
    
    return(file)

C = splitdata(C)
W = splitdata(W)
D = splitdata(D)
G = splitdata(G)

def name_list(x):
    return_list = []
    for item in x:
        return_list.append(item[1])

    return return_list
    

names_C = name_list(C)
names_W = name_list(W)
names_D = name_list(D)
names_G = name_list(G)

names_all = names_C + names_D + names_G + names_W

#combo_2C = list(i.combinations(names_C,2))
#combo_3C = list(i.combinations(names_C,3))
#combo_3W = list(i.combinations(names_W,3))
#combo_4W = list(i.combinations(names_W,4))
#combo_2D = list(i.combinations(names_D,2))
#combo_3D = list(i.combinations(names_D,3))




