import matplotlib.pyplot as plt
import numpy as np
import csv

from matplotlib import collections


def retrieveCSV(file, max):
    #row 0=>p, 1=>d, 2=>q, 3=>P, 4=>D, 5=>Q,6=>S, 7=>Time, 8=>AIC
    xValue=[]
    timeValue=[]
    i=0
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if i>=max:
                break
            else:
                xValue.append("({})".format(row[3]+row[4]+row[5]))
                timeValue.append(row[7])
                print(row)
                i=i+1
        xValue.pop(0)
        timeValue.pop(0)
    dict={}
    for i in range(len(xValue)):
        dict[xValue[i]]=timeValue[i]
    sortDict=sorted(dict.items(), key=lambda t: t[1])
    print(sortDict)
    print(sortDict[0][0])
    names=[]
    values=[]
    for i in range(len(sortDict)):
        names.append(sortDict[i][0])
        values.append(sortDict[i][1])

    print(names)
    print(values)
    fig, ax=plt.subplots(figsize=(55,20))
    ax.plot(names, values)
    ax.set_xlabel('Hyperparamètres')
    ax.set_ylabel('Temps')
    ax.set_title('Temps d\'exécution par séquence d\'hyperparamètres')
    fig.tight_layout()
    plt.savefig("../data/log_performance.png")
    plt.show()

retrieveCSV("log_perf.log", 200)