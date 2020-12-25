import os
import pandas as pd
import xgboost
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn import preprocessing 
from sklearn.model_selection import GridSearchCV

output_player = open('player_feature_weights.txt','w')
output_goalie = open('goalie_feature_weights.txt','w')
mingw_path = 'C:\\Program Files\\mingw-w64\\x86_64-7.3.0-posix-seh-rt_v5-rev0\\mingw64\\bin'
os.environ['PATH'] = mingw_path + ';' + os.environ['PATH']
seed = 1

# Player Section
X_test = pd.read_csv("players_table_test.csv", header=0)

df = pd.read_csv("players_table.csv", header=0)
Y = df['DKScore']
X = df.drop('DKScore',  axis=1)

X_train, X_dev, y_train, y_dev = train_test_split(X, Y, test_size=0.1, random_state=seed)

print ('Training Player reg')

reg = xgboost.XGBRegressor()

"""parameters = {'max_depth': [1,2,4,6,8], 'subsample':[0.25,0.5,0.75,1], 'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5]}
grid_obj = GridSearchCV(reg, parameters)
grid_obj = grid_obj.fit(X_train, y_train)
reg = grid_obj.best_estimator_
"""

print ("X_train has size", X_train.shape, "y_train has size", y_train.shape)
reg.fit(X_train, y_train)

for feature_weights, category in sorted(zip(reg.feature_importances_, list(X_train)),key=lambda x: x[0], reverse = True):
    output_player.write(str(feature_weights) + '\t' + category +'\n')

y_pred = reg.predict(X_dev)
print('For dev set ', mean_squared_error(y_dev,y_pred))

print ("X_test has size", X_test.shape, "Now testing...")
y_pred = reg.predict(X_test)

X_test['DKScore'] = y_pred
X_test['playerName'] = X_test[[pnames for pnames in X_test.columns if 'playerName' in pnames]].idxmax(axis=1)
X_test['playerName'] = X_test['playerName'].str[11:]
X_test.to_csv("player_result.csv", header=True, index=False, columns=['playerName','DKScore'])



# Goalies Section



X_test = pd.read_csv("goalies_table_test.csv", header=0)
df = pd.read_csv("goalies_table.csv", header=0) #(query_string, conn)

Y = df['DKScore']
X = df.drop('DKScore', axis=1)

X_train, X_dev, y_train, y_dev = train_test_split(X, Y, test_size=0.05, random_state=seed)

print ('Training Goalie reg')

reg = xgboost.XGBRegressor() 

"""parameters = {'max_depth': [1,2,4,6,8], 'subsample':[0.25,0.5,0.75,1], 'learning_rate': [0.1, 0.2, 0.3, 0.4, 0.5]}
grid_obj = GridSearchCV(reg, parameters)
grid_obj = grid_obj.fit(X_train, y_train)
reg = grid_obj.best_estimator_"""

print ("X_train has size", X_train.shape, "y_train has size", y_train.shape)
reg.fit(X_train, y_train)

for feature_weights, category in sorted(zip(reg.feature_importances_, list(X_train)),key=lambda x: x[0], reverse = True):
    output_goalie.write(str(feature_weights) + '\t' + category +'\n')

y_pred = reg.predict(X_dev)
print('For dev set ', mean_squared_error(y_dev,y_pred))

print ("X_test has size", X_test.shape, "Now testing...")
y_pred = reg.predict(X_test)

X_test['DKScore'] = y_pred
X_test['playerName'] = X_test[[pnames for pnames in X_test.columns if 'playerName' in pnames]].idxmax(axis=1)
X_test['playerName'] = X_test['playerName'].str[11:]
X_test.to_csv("goalie_result.csv", header=True, index=False, columns=['playerName','DKScore'])



