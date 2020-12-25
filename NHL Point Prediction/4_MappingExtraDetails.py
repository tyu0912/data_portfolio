import pickle
import numpy as np
import sqlite3
import pandas as pd

#conn = sqlite3.connect('game_data.sqlite')
#cur = conn.cursor()
#query_string = "select * from player_result"
#data = pd.read_sql(query_string, conn)

data = pd.read_csv("player_result.csv", header=0)

DK_data = pd.read_csv('DK_Input/players_playing.txt', sep="\t", header=None)
DK_data.columns = ['playerName','DK_Id','Position','DK_Value','Game','Team','OpponentTeam','DK_points']

DK_data = DK_data.drop(columns=['DK_Id','Game'])

merge1 = pd.merge(data, DK_data, on=['playerName'], how='inner')


active_data = pd.read_csv('Rotogrind_Scrape/active_players.txt', sep="\t", header=None)
active_data.columns = ['playerName']


merge2 = pd.merge(merge1, active_data, on=['playerName'], how='inner')


played_filter = pd.read_csv('playersgames_played_filter.csv', sep=",", header=None)
played_filter.columns = ['playerName']

merge3 = pd.merge(merge2, played_filter, on=['playerName'], how='inner')


positions = ['W','C','D']

for position in positions:
    output = merge3[merge3['Position'] == position]
    output = output.sort_values('DKScore', ascending=False)
    output = output.head(50)
    output_name = 'Final Results/' + position + '.txt'
    output.to_csv(output_name,sep='\t', header=False, columns=['playerName','DKScore','DK_Value','Team','OpponentTeam','DK_points'])


###################### Goalies


#query_string = "select * from goalie_result"
#data = pd.read_sql(query_string, conn)

data = pd.read_csv("goalie_result.csv", header=0)

DK_data = pd.read_csv('DK_Input/goalies_playing.txt', sep="\t", header=None)
DK_data.columns = ['playerName','DK_Id','Position','DK_Value','Game','Team','OpponentTeam','DK_points']

DK_data = DK_data.drop(columns=['DK_Id','Game'])

merge1 = pd.merge(data, DK_data, on=['playerName'], how='inner')

active_data = pd.read_csv('Rotogrind_Scrape/active_players.txt', sep="\t", header=None)
active_data.columns = ['playerName']

merge2 = pd.merge(merge1, active_data, on=['playerName'], how='inner')

played_filter = pd.read_csv('goaliesgames_played_filter.csv', sep=",", header=None)
played_filter.columns = ['playerName']

merge3 = pd.merge(merge2, played_filter, on=['playerName'], how='inner')

positions = ['G']

for position in positions:
    output = merge3[merge3['Position'] == position]
    output = output.sort_values('DKScore', ascending=False)
    output = output.head(1)
    output_name = 'Final Results/' + position + '.txt'
    output.to_csv(output_name,sep='\t', header=False, columns=['playerName','DKScore','DK_Value','Team','OpponentTeam','DK_points'])