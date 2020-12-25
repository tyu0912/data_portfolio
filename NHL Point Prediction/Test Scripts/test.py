import pandas as pd
import sqlite3

conn = sqlite3.connect('game_data.sqlite')
cur = conn.cursor()

p_df = pd.read_sql('select playerBirthDate from players_table', conn)

df['Age'] = (date.today() - pd.to_datetime(df['playerBirthDate']))
    print (df['Age'])