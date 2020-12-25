import pulp as p

out = open('choices_no_gt_considered.txt','w')
out2 = open('choices_gt_considered.txt','w')

C = open('C.txt','r').read().splitlines()
W = open('W.txt','r').read().splitlines()
D = open('D.txt','r').read().splitlines()
G = open('G.txt','r').read().splitlines()

def splitdata(file):
    for index,line in enumerate(file):
        file[index] = line.split('\t')
    
    return(file)

def make_orig_dict(input_list, y):
    output = {}
    for x in input_list:
        if x[y].isalpha():
            output[x[1]] = (x[y])
        else:
            output[x[1]] = float(x[y])


    return output

def make_list_names(input_list,y):
    names = []
    for x in input_list:
        names.append(x[y])

    return names

C = splitdata(C)
W = splitdata(W)
D = splitdata(D)
G = splitdata(G)

list_C_names = make_list_names(C,1)
list_W_names = make_list_names(W,1)
list_D_names = make_list_names(D,1)
list_G_names = make_list_names(G,1)
#list_teams = list(set(make_list_names(C,4)))

dict_C_value = make_orig_dict(C,2)
dict_W_value = make_orig_dict(W,2)
dict_D_value = make_orig_dict(D,2)
dict_G_value = make_orig_dict(G,2)


dict_C_cost = make_orig_dict(C,3)
dict_W_cost = make_orig_dict(W,3)
dict_D_cost = make_orig_dict(D,3)
dict_G_cost = make_orig_dict(G,3)


dict_C_team = make_orig_dict(C,4)
dict_W_team = make_orig_dict(W,4)
dict_D_team = make_orig_dict(D,4)
dict_G_team = make_orig_dict(G,4)

dict_G_opp = make_orig_dict(G,5)

dict_C_dkp = make_orig_dict(C,6)
dict_W_dkp = make_orig_dict(W,6)
dict_D_dkp = make_orig_dict(D,6)
dict_G_dkp = make_orig_dict(G,6)

def optimization(out_num):
    c = p.LpVariable.dicts("c", indexs = list_C_names, lowBound=0, upBound=1, cat='Integer', indexStart=[] )
    w = p.LpVariable.dicts("w", indexs = list_W_names, lowBound=0, upBound=1, cat='Integer', indexStart=[] )
    d = p.LpVariable.dicts("d", indexs = list_D_names, lowBound=0, upBound=1, cat='Integer', indexStart=[] )
    g = p.LpVariable.dicts("g", indexs = list_G_names, lowBound=0, upBound=1, cat='Integer', indexStart=[] )

    #t = p.LpVariable.dicts("t", indexs = list_teams, lowBound=0, upBound=1, cat='Integer', indexStart=[] )

    prob = p.LpProblem('Player Selection',p.LpMaximize)

    prob += p.lpSum( [ c[i]*(dict_C_value[i]+dict_C_dkp[i])/2 for i in list_C_names ] + [ w[j]*(dict_W_value[j]+dict_W_dkp[j])/2 for j in list_W_names ] +  [ d[k]*(dict_D_value[k]+dict_D_dkp[k])/2 for k in list_D_names ] + [ g[l]*(dict_G_value[l]+dict_G_dkp[l])/2 for l in list_G_names ]), " Objective is sum of prices of selected items "
    #prob += p.lpSum( [ c[i]*dict_C_value[i] for i in list_C_names ] + [ w[j]*dict_W_value[j] for j in list_W_names ] +  [ d[k]*dict_D_value[k] for k in list_D_names ] + [ g[l]*dict_G_value[l] for l in list_G_names ]), " Objective is sum of prices of selected items "


    prob += p.lpSum( [ c[i] for i in list_C_names ] ) >= 2, " Constraint is that we choose >=2 centers "
    prob += p.lpSum( [ w[j] for j in list_W_names ] ) >= 3, "Constraint is that we choose >=3 wingers "
    prob += p.lpSum( [ d[k] for k in list_D_names ] ) == 2, "Constraint is that we choose >=2 defense "

    prob += p.lpSum( [ c[i] for i in list_C_names ] ) <= 3, " Constraint is that we choose <= 3centers "
    prob += p.lpSum( [ w[j] for j in list_W_names ] ) <= 4, "Constraint is that we choose <= 4 wingers "
    #prob += p.lpSum( [ d[k] for k in list_D_names ] ) <= 3, "Constraint is that we choose <= 3 defense "

    prob += p.lpSum( [ g[l] for l in list_G_names ] ) == 1, "Constraint is that we choose 1 goalie "
    prob += p.lpSum( [ c[i]*dict_C_cost[i] for i in list_C_names ] + [ w[j]*dict_W_cost[j] for j in list_W_names ] +  [ d[k]*dict_D_cost[k] for k in list_D_names ] + [ g[l]*dict_G_cost[l] for l in list_G_names ]) <= 50000, " Cost Restriction "
    prob += p.lpSum( [ c[i] for i in list_C_names ] + [ w[j] for j in list_W_names ] +  [ d[k] for k in list_D_names ] + [ g[l] for l in list_G_names ]) == 9, " Choice Restriction "

    #prob += p.lpSum( c[i]*dict_C_team for i in list_C_names)
    p.solvers.YAPOSIB()

    prob.solve()

    outlist=[]
    for v in prob.variables():
        print (v.name, "=", v.varValue)
        if v.varValue == 1:
            outlist.append(v.name)
            if out_num == 0:
                out.write(v.name + '\n')
            else:
                out2.write(v.name + '\n')
    
    

    print ("Status:", p.LpStatus[ prob.status ])

    return outlist

outlist = optimization(0)

for player in outlist:
    if player.find('g_') == 0:
        player = player[player.find('g_')+2:].replace('_',' ')
        goalie_opp = dict_G_opp[player]
    else:
        continue

rerun = 0     

for player in outlist:
    player = player[player.find('_')+1:].replace('_',' ')
    dict_all_team = {**dict_C_team,**dict_W_team,**dict_D_team,**dict_G_team}
    if dict_all_team[player] == goalie_opp:
        rerun = 1
        break
    else:
        continue

if rerun == 0:
    out2.write('No conflict')
else:
    
    dict_C_value = { k:v for k, v in dict_C_value.items() if dict_all_team[k] != goalie_opp }
    dict_W_value = { k:v for k, v in dict_W_value.items() if dict_all_team[k] != goalie_opp }
    dict_D_value = { k:v for k, v in dict_D_value.items() if dict_all_team[k] != goalie_opp }
    dict_G_value = { k:v for k, v in dict_G_value.items() if dict_all_team[k] != goalie_opp }

    dict_C_cost = { k:v for k, v in dict_C_cost.items() if dict_all_team[k] != goalie_opp }
    dict_W_cost = { k:v for k, v in dict_W_cost.items() if dict_all_team[k] != goalie_opp }
    dict_D_cost = { k:v for k, v in dict_D_cost.items() if dict_all_team[k] != goalie_opp }
    dict_G_cost = { k:v for k, v in dict_G_cost.items() if dict_all_team[k] != goalie_opp }

    list_C_names = [k for k in list_C_names if dict_all_team[k] != goalie_opp]
    list_W_names = [k for k in list_W_names if dict_all_team[k] != goalie_opp]
    list_D_names = [k for k in list_D_names if dict_all_team[k] != goalie_opp]
    list_G_names = [k for k in list_G_names if dict_all_team[k] != goalie_opp]

    optimization(1)
