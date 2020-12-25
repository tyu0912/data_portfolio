import pickle
import pandas as pd
import xgboost
import numpy as np
import sqlite3

model = pickle.load(open('player_model.sav', 'rb'))



df = pd.read_csv("players_table_test.csv", header=0)

opponent_cols = [col for col in df.columns if 'opponent' in col]

for team in opponent_cols:
    df[team] = 0

for line in players:
    items = line.split('\t')
    player = 'playerName_' + items[0]
    opponent = 'opponentTeamAbbrev_' + items[6]
    try:
        df.loc[df[player] != 0, opponent] = 1
    except:
        continue

y_pred = model.predict(df.reindex_axis(sorted(df.columns), axis=1))

df['DK_Score'] = y_pred
#df['playerName'] = df[[pnames for pnames in df.columns if 'playerName' in pnames]].idxmax(axis=1)
print (df)

df.to_csv("player_result.csv", header=True)
quit()


#################### Goalie 

model = pickle.load(open('goalie_model.sav', 'rb'))

players = open('DK_Input/goalies_playing.txt').read()
players = players.splitlines()

df = pd.read_csv("goalies_table_test.csv", header=0)


opponent_cols = [col for col in df.columns if 'opponent' in col]

for team in opponent_cols:
    df[team] = 0

for line in players:
    items = line.split('\t')
    player = 'playerName_' + items[0]
    opponent = 'opponentTeamAbbrev_' + items[6]
    try:
        df.loc[df[player] != 0, opponent] = 1
    except:
        continue

y_pred = model.predict(df)

df['DK_Score'] = y_pred
#df['playerName'] = df[[pnames for pnames in df.columns if 'playerName' in pnames]].idxmax(axis=1)

df.to_csv("goalie_result.csv", header=True)