import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('winemag-data-130k-v2.csv', index_col = 0)
df = df.sample(frac=0.3, replace=False)

print (df.columns.values)
print(len(df['region_1'].unique()))

#fig, axs = plt.subplots(2, 2, figsize=(2, 2), sharey=True)
#axs[0,0].scatter(df['points'],df['price'])

#ax = sns.boxplot(x="region_1", y="price", data=df)

#axs[0,1].boxplot(df['region_1'],df['price'])
#axs[1,0].bar(df['region_2'],df['price'])
#axs[1,1].bar(df['country'],df['price'])


#plt.show()












#plt.show(block=False)
#input('press <ENTER> to continue')

