import sys
sys.path.insert(0, '../functions')

import functions as f

data = f.pd.read_csv("../Human Resources Analytics/HR_comma_sep.csv", header=0)

print("\n Here are some basic statistics \n")
print (data.head())
print (data.describe())

f.get_corrchart(data)



data['salary'] = f.text2value(data['salary'])
data['sales'] = f.text2value(data['sales'])


