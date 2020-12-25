import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns


def text2value(colname):
    items = list(set(colname))
    mapdict = dict()
    for index, item in enumerate(sorted(items)):
        print("The item: " + item + " is assigned to " + str(index))
        mapdict[item] = index

    colname = colname.map(mapdict)
    return colname

def get_corrchart(data):
    corr = data.corr()
    sns.heatmap(data.corr(), xticklabels=corr.columns.values, yticklabels=corr.columns.values)

    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

