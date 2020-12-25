import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing

data_train = pd.read_csv('train.csv')
data_test = pd.read_csv('test.csv')

#Data Exploration

print ('The original data looks like: \n', data_train.head(20))



quit()
### Data Transformation

def simplify_ages(df):
    
    df.Age = df.Age.fillna(df.Age.mean())
    df.Age = (df.Age - df.Age.min())/(df.Age.max()-df.Age.min())

    #df.Age = df.Age.fillna(-0.5)
    #bins = (-1, 0, 5, 12, 18, 35, 60, 120)
    #group_names = ['Unknown', 'Baby', 'Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']
    #categories = pd.cut(df.Age, bins, labels=group_names)
    #df.Age = categories
    
    return df

def simplify_cabins(df):
    df.Cabin = df.Cabin.fillna('N')
    df.Cabin = df.Cabin.apply(lambda x: x[0])
    return df

def simplify_fares(df):
    df.Fare = df.Fare.fillna(df.Fare.mean())
    df.Fare = (df.Fare-df.Fare.min())/(df.Fare.max()-df.Fare.min())
    
    #df.Fare = df.Fare.fillna(-0.5)
    #bins = (-1, 0, 8, 15, 31, 1000)
    #group_names = ['Unknown', '1_quartile', '2_quartile', '3_quartile', '4_quartile']
    #categories = pd.cut(df.Fare, bins, labels=group_names)
    #df.Fare = categories
    
    return df

def format_name(df):
    df['Lname'] = df.Name.apply(lambda x: x.split(' ')[0])
    df['NamePrefix'] = df.Name.apply(lambda x: x.split(' ')[1])

    df['NamePrefix'] = df['NamePrefix'].replace({'Ms.': 'Mrs.'})
    df.loc[df.groupby('NamePrefix').NamePrefix.transform('count').lt(10), 'NamePrefix'] = 'Other'

    df['NamePrefix'].value_counts().plot(kind='bar')

    return df

def analyze_family(df):
    df['family_size'] = df["SibSp"] + df["Parch"] + 1
    df['family_size'] = df['family_size'].map(lambda x: 'single' if x == 1 else 'small' if 2 <= x <= 4 else 'large')
    #g = sns.factorplot(x="family_size",y="Survived",data = df)
    #g = g.set_ylabels("Survival Probability")
    #plt.show()
    return df 

def getDummies(df):
    return pd.get_dummies(df, columns=['NamePrefix', 'family_size','Cabin','Sex'])

def drop_features(df):
    return df.drop(['Ticket', 'Name', 'Embarked', "SibSp", "Parch", "Lname"], axis=1)


""" def encode_features(df_train, df_test):
    features = ['Cabin', 'Sex', 'NamePrefix', 'family_size']
    df_combined = pd.concat([df_train[features], df_test[features]])
    
    for feature in features:
        le = preprocessing.LabelEncoder()
        le = le.fit(df_combined[feature])
        df_train[feature] = le.transform(df_train[feature])
        df_test[feature] = le.transform(df_test[feature])
    return df_train, df_test """

def transform_features(df):
    df = simplify_ages(df)
    df = simplify_cabins(df)
    df = simplify_fares(df)
    df = format_name(df)
    df = analyze_family(df)
    df = drop_features(df)
    df = getDummies(df)

    return df


data_train = transform_features(data_train)
data_test = transform_features(data_test)

print('\n After transformations my data looks like: \n', data_train.head())

#data_train, data_test = encode_features(data_train, data_test)


### Splitting the data
from sklearn.model_selection import train_test_split

X_all = data_train.drop(['Survived', 'PassengerId'], axis=1)
y_all = data_train['Survived']

num_test = 0.20
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, test_size=num_test, random_state=10)
print('Size of X_train is: ' + str(X_train.size), "Size of X_test is: " + str(X_test.size) )


### Machine Learning Part.
 
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import make_scorer, accuracy_score, confusion_matrix

from sklearn.model_selection import KFold

def run_kfold(clf):
    kf = KFold(n_splits=10, random_state=10, shuffle=False)
    outcomes = []
    fold = 0
    for train_index, test_index in kf.split(X_all):
        fold += 1
        X_train, X_test = X_all.values[train_index], X_all.values[test_index]
        y_train, y_test = y_all.values[train_index], y_all.values[test_index]
        classifier.fit(X_train, y_train)
        predictions = classifier.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        outcomes.append(accuracy) 
    mean_outcome = np.mean(outcomes)

    return mean_outcome

classifiers = {
    'RandomForestClassifier': RandomForestClassifier(), 
    'ExtraTreesClassifier': ExtraTreesClassifier(),
    'KNeighborsClassifier': KNeighborsClassifier(), 
    'GradientBoostingClassifier': GradientBoostingClassifier(), 
    'AdaBoostClassifier': AdaBoostClassifier(),
    'MLPClassifier': MLPClassifier(),
    'SGDClassifier': SGDClassifier(),
    'LogisticRegression': LogisticRegression(),
    'BernoulliNB': BernoulliNB(),
    'MultinomialNB': MultinomialNB()
    }

scores = {}

for name, classifier in classifiers.items():
    kfold_mean = run_kfold(classifier)
    scores[name] = kfold_mean

sorted_scores = sorted(scores.items(), key=lambda kv: round(kv[1],3), reverse = True)

print('\n The top 5 training algorithms appears to be: \n', sorted_scores[0:5])

### Prepare grid search parameters:

parameters = {
    'RandomForestClassifier': {'n_estimators': [4, 6, 9], 'max_features': ['log2', 'sqrt','auto'], 'criterion': ['entropy', 'gini'],'max_depth': [2, 3, 5, 10], 'min_samples_split': [2, 3, 5],'min_samples_leaf': [1,5,8]}, 
    'ExtraTreesClassifier': {'n_estimators': [2, 4, 6, 8], 'max_features': ['log2', 'sqrt','auto'], 'criterion': ['entropy', 'gini'],'max_depth': [2, 3, 5, 10], 'min_samples_split': [2, 3, 5],'min_samples_leaf': [1,5,8]},
    'KNeighborsClassifier':  {'n_neighbors': [2], 'weights': ['uniform','distance'],'algorithm':['auto','ball_tree', 'kd_tree', 'brute']}, 
    'GradientBoostingClassifier': {'loss' : ["deviance"],'n_estimators' : [100,200,300],'learning_rate': [0.1, 0.05, 0.01],'max_depth': [4, 8],'min_samples_leaf': [100,150],'max_features': [0.3, 0.1] }, 
    'AdaBoostClassifier': {'n_estimators': [1,2,4,8,16,32]},
    'LogisticRegression': {'solver': ['newton-cg', 'lbfgs', 'sag', 'saga'], 'multi_class': ['ovr', 'multinomial']},
    'MLPClassifier': {'activation' : ['identity', 'logistic', 'tanh', 'relu'], 'hidden_layer_sizes': [(100,),(200,),(500,),(750,),(1000,)], 'shuffle':[True,False]},
    'SGDClassifier': {'loss': ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron'], 'penalty':['none', 'l2', 'l1', 'elasticnet'], 'alpha': [0.001,0.01,0.1,1,10,50]},
    'BernoulliNB': {'alpha': [0,0.01,0.1,1,10,50]},
    'MultinomialNB': {'alpha': [0,0.01,0.1,1,10,50]}, 
}

acc_scorer = make_scorer(accuracy_score)
best_estimators = {}

for k,v in sorted_scores[0:10]:
    grid_obj = GridSearchCV(classifiers[k], parameters[k], scoring=acc_scorer)
    grid_obj = grid_obj.fit(X_train, y_train)

    # Set the clf to the best combination of parameters
    
    best_estimators[k] = grid_obj.best_estimator_
    
    classifier = grid_obj.best_estimator_
    classifier.fit(X_train, y_train)
    predictions = classifier.predict(X_test)

    print('With optimal paramters - ', k,':', accuracy_score(y_test, predictions))
    print(confusion_matrix(y_test, predictions))

eclf1 = VotingClassifier(estimators=[(k,v) for k,v in best_estimators.items()])
eclf1 = eclf1.fit(X_train, y_train)
predictions = eclf1.predict(X_test)

print('With voting: ', accuracy_score(y_test, predictions))
print(confusion_matrix(y_test, predictions))

