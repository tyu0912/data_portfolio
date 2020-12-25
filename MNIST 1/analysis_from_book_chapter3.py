import pandas as pd
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

MNIST = pd.read_csv('train.csv')

y = MNIST['label']
X = MNIST.ix[:, MNIST.columns != 'label']

X_train, X_test, y_train, y_test = X.head(32000), X.tail(10000), y.head(32000), y.tail(10000)

shuffle_index = np.random.permutation(32000)

X_train = X_train.reindex(shuffle_index)
y_train = y_train.reindex(shuffle_index)

pd

y_train_5 = pd.Series(np.where(y_train.values == 5, 1, 0), y_train.index)
y_test_5 = pd.Series(np.where(y_test.values == 5, 1, 0), y_test.index)

y_train_5 = y_train_5.reshape((32000,1))

#print(X_train.shape)
#print(y_train_5)
#quit()

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train,y_train_5)

print(cross_val_score(sgd_clf, X_train, y_train_5.ravel(), cv=3, scoring="accuracy"))

y_train_pred = cross_val_predict(sgd_clf,X_train,y_train_5, cv=3)

print(confusion_matrix(y_train_5,y_train_pred))

y_scores = cross_val_predict(sgd_clf,X_train,y_train_5, cv=3, method="decision_function")

print(y_scores)

precisions, recalls, thresholds = precision_recall_curve(y_train_5, y_scores)

def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1],"b--",label="Precision")
    plt.plot(thresholds,recalls[:-1],"g-",label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="upper left")
    plt.ylim([0,1])

plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
plt.show()

y_train_pred_90 = (y_scores > 80000)

print(precision_score(y_train_5,y_train_pred_90))
print(recall_score(y_train_5,y_train_pred_90))

fpr, tpr, thresholds = roc_curve(y_train_5,y_scores)

def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0,1], [0,1], 'k--')
    plt.axis([0,1,0,1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

forest_clf = RandomForestClassifier(random_state=42)
y_probas_forest = cross_val_predict(forest_clf, X_train, y_train_5, cv=3, method="predict_proba")

y_scores_forest = y_probas_forest[:,1]
fpr_forest, tpr_forest, thresholds_forest = roc_curve(y_train_5,y_scores_forest)

plt.plot(fpr, tpr, "b:",label="SGD")
plot_roc_curve(fpr_forest, tpr_forest, "Random Forest")
plt.legend(loc="bottom right")
plt.show()

print(roc_auc_score(y_train_5,y_scores_forest))

################ Multiclass Classification

sgd_clf.fit(X_train, y_train)
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train.astype(np.float64))
print(cross_val_score(sgd_clf, X_train_scaled, y_train, cv=3, scoring="accuracy"))

y_train_pred = cross_val_predict(sgd_clf, X_train_scaled, y_train, cv=3)
conf_mx = confusion_matrix(y_train, y_train_pred)
plt.matshow(conf_mx, cmap=plt.cm.gray)
plt.show()

row_sums = conf_mx.sum(axis=1, keepdims=True)
norm_conf_mx = conf_mx/row_sums

np.fill_diagonal(norm_conf_mx, 0)
plt.matshow(norm_conf_mx, cmap=plt.cm.gray)
plt.show()

y_train_large = pd.Series(np.where(y_train.values >= 7, 1, 0), y_train.index)
y_train_odd = pd.Series(np.where(y_train.values % 2 == 1, 1, 0), y_train.index)
y_multilabel = pd.concat([y_train_large, y_train_odd], axis=1).as_matrix()


knn_clf = KNeighborsClassifier()
knn_clf.fit(X_train, y_multilabel)

y_train_knn_pred = cross_val_predict(knn_clf, X_train, y_train, cv=3)
f1score = f1_score(y_train, y_train_knn_pred, average="macro")

print(f1score)

noise = np.random.randint(0,100, len(X_train),784)
noise = np.random.randint(0,100,(len(X_test),784))

X_train_mod = X_train + noise
X_test_mod = X_test + noise
y_train_mod = X_train
y_test_mod = X_test

knn_clf.fit(X_train_mod,y_train_mod)
clean_digit = knn_clf.predict([X_test_mod[some_index]])
plot_digit(clean_digit)

def show_number(x):
    some_digit = X.iloc[x].values.reshape(28,28)

    plt.imshow(some_digit, cmap = plt.cm.binary, interpolation="nearest")
    plt.axis("off")
    plt.show()

