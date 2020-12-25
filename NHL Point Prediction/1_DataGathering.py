import json
import pandas as pd
import numpy as np
from datetime import date,timedelta
from urllib.request import urlopen
from functools import reduce


season_end = str(date.today())
season_start = str(date.today() - timedelta(days=365))

if date.today().month in [9,10,11,12]:
    season = str(date.today().year) + str(date.today().year + 1)
else:
    season = str(date.today().year - 1) + str(date.today().year)


drop_list = open("1_columns_remove.txt",'r').read().splitlines()
categorical_list = open("1_convert_categorical.txt",'r').read().splitlines()
normalize_list = open("1_normalize_values.txt",'r').read().splitlines()
players = open('DK_Input/players_playing.txt').read().splitlines()

player_dic = {}
goalies_dic = {}
summary = {}

player_dic['Summary'] = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&sort=[{%22property%22:%22points%22,%22direction%22:%22DESC%22},{%22property%22:%22goals%22,%22direction%22:%22DESC%22},{%22property%22:%22assists%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%22'+season_start+'%22%20and%20gameDate%3C=%22'+season_end+'%22%20and%20gameTypeId=2'
player_dic['Hits'] = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=realtime&sort=[{%22property%22:%22hits%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%22'+season_start+'%22%20and%20gameDate%3C=%22'+season_end+'%22%20and%20gameTypeId=2'
player_dic['Faceoffs'] = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=faceoffs&sort=[{%22property%22:%22faceoffs%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%22'+season_start+'%22%20and%20gameDate%3C=%22'+season_end+'%22%20and%20gameTypeId=2'
player_dic['Shootouts'] = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=shootout&isGame=true&reportName=skatershootout&sort=[{%22property%22:%22shootoutGoals%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%22'+season_start+'%22%20and%20gameDate%3C=%22'+season_end+'%22%20and%20gameTypeId=2'

goalies_dic['Goalies'] = 'http://www.nhl.com/stats/rest/goalies?isAggregate=false&reportType=goalie_basic&isGame=true&reportName=goaliesummary&sort=[{%22property%22:%22wins%22,%22direction%22:%22DESC%22}]&cayenneExp=gameDate%3E=%22'+season_start+'%22%20and%20gameDate%3C=%22'+season_end+'%22%20and%20gameTypeId=2'

summary['players'] = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=false&reportName=skatersummary&cayenneExp=gameTypeId=2%20and%20seasonId%3E='+ season +'%20and%20seasonId%3C=' + season
summary['goalies'] = 'http://www.nhl.com/stats/rest/goalies?isAggregate=false&reportType=goalie_basic&isGame=false&reportName=goaliesummary&cayenneExp=gameTypeId=2%20and%20seasonId%3E='+ season +'%20and%20seasonId%3C=' + season


# Make filter table for players > 25 games and goalies > 20 games. 

for k,v in summary.items():
    print (v)
    raw_data = json.load(urlopen(v))
    df = pd.DataFrame(raw_data['data'])
    output_str = k + 'games_played_filter.csv'
    if k == 'players':
        df = df[df['gamesPlayed'] >= 1]
    else: 
        df = df[df['gamesPlayed'] >= 1]
    df['playerName'].to_csv(output_str, index=False)


def generate_df(url):
    raw_data = json.load(urlopen(url))
    df = pd.DataFrame(raw_data['data'])
    df['gameDate'] = pd.to_datetime(df['gameDate'].str.slice(start=0, stop=10), format='%Y-%m-%d')
    df['age'] = (df['gameDate'] - pd.to_datetime(df['playerBirthDate']))/365
    df['age'] = df['age'].dt.days.astype('float64')

    return df 

def drop_columns(list, df):
    df = df.drop(drop_list, axis=1, errors="ignore")
    #df = df.fillna(0)
    return df

def convert_categorical(list,df):
    return (pd.get_dummies(df, columns= list))

def normalize(list, df):
    for item in list:
        try:
            df[item] = (df[item] - df[item].mean())/df[item].std()
        except:
            pass

    return df

def make_traindevdata(df, tables):
    df = pd.concat([d.set_index(['playerId', 'gameId']) for d in tables], axis=1).reset_index()
    df = df.loc[:, ~df.columns.duplicated()]
    df = convert_categorical(categorical_list,df)
    df = normalize(normalize_list, df)

    return df

def update_opponents(df):
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

    return df

def make_testdata(df):
    df = df.sort_values(by=['playerId','gameDate'], ascending=[1, 0])
    df = df.groupby('playerId').head(10)
    df = df.groupby('playerId').agg('mean').reset_index(drop=False)
    df = update_opponents(df)
    
    return df

def drop_and_score(df_dev, df_test, type):
    if type == 'player':
        df_dev['DKScore'] = df_dev['goals']*3 + df_dev['assists']*2 + df_dev['shots']*0.5 + df_dev['blockedShots']*0.5 + df_dev['shPoints']*1 + df_dev['shootoutGoals'].fillna(0)*0.2 + (df_dev['goals'] >= 3)*1.5
    else:
        df_dev['DKScore'] = df_dev['wins']*3 + df_dev['saves']*0.2 - df_dev['goalsAgainst']*1 + (df_dev['goalsAgainst'] == 0)*2
    
    df_dev = drop_columns(drop_list, df_dev)
    df_test = drop_columns(drop_list, df_test)

    return df_dev, df_test




# Create player files

tables = []

for k,v in player_dic.items():
    new_df = generate_df(v)
    tables.append(new_df)


df_traindev = make_traindevdata(df, tables)
df_testdata = make_testdata(df_traindev)

df_traindev, df_testdata = drop_and_score(df_traindev, df_testdata, 'player')

df_testdata.to_csv("players_table_test.csv", header=True, index=False)
df_traindev.to_csv("players_table.csv", header=True, index=False)


# Create goalie files

tables = []

for k,v in goalies_dic.items():
    new_df = generate_df(v)
    tables.append(new_df)

df_traindev = make_traindevdata(df, tables)
df_testdata = make_testdata(df_traindev)

df_traindev, df_testdata = drop_and_score(df_traindev, df_testdata, 'goalie')

df_testdata.to_csv("goalies_table_test.csv", header=True, index=False)
df_traindev.to_csv("goalies_table.csv", header=True, index=False)




