import pandas as pd
import sqlite3


conn = sqlite3.connect('game_data.sqlite')
cur = conn.cursor()

p_df = pd.read_csv("players_table.csv", header=0)

zero_list = open("1.1_columns_fill0.txt").read().splitlines()
zero_map = {}
for item in zero_list:
    print (item)
    x, y = item.split(',')
    zero_map[x] = y 


p_df.fillna(value=zero_map, inplace=True)

p_df.to_csv("players_table.csv", header=True)