import pandas as pd
import pyodbc as py

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=SQLSRV01;DATABASE=DATABASE;UID=USER;PWD=PASSWORD')
cursor = cnxn.cursor()

cursor.execute("SELECT WORK_ORDER.TYPE,WORK_ORDER.STATUS, WORK_ORDER.BASE_ID, WORK_ORDER.LOT_ID FROM WORK_ORDER")
for row in cursor.fetchall():
    print (row)


df = pd.read_sql('SELECT * FROM table_name', con=cnxn)
df.to_sql(name, con, if_exists='replace',schema='DB')
