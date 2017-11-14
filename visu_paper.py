# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:28:33 2017

@author: mducoffe

visu curve
"""

import numpy as np
import pylab as pl

#%%
# step 1 read csv file
from contextlib import closing
import csv
import os


filename="random.csv"
def get_actif_data(repository, filename):

    x_labels=[]
    y_acc=[]
    y_max = 0
    with closing(open(os.path.join(repository, filename))) as f:
        csv_f = csv.reader(f, delimiter=';', quotechar='|')
    
        for row in csv_f:
            x, y = int(row[0]), float(row[1])
            if x>5000:
                break
            """
            if y <0.25 and x >600:
                continue
            """
            if y < y_max:
                y = y_max
            else:
                y_max = y
            x_labels.append(x)
            y_acc.append(y)
    return x_labels, y_acc
#%%
repository="data/csv"
dataset='MNIST'
network='VGG'
methods = ['random', 'egl', 'uncertainty', 'aaq', 'saaq']
filenames =['{}_{}_'.format(dataset, network)+str(method)+'.csv' for method in methods]
#filenames=['CIFAR_VGG_random.csv', 'CIFAR_VGG_egl.csv', 'CIFAR_LeNet5_uncertainty.csv']
legends=methods
linestyles=['r-', 'b-', 'g--', 'k--', 'p-']
dico_actif={}

for filename, legend, linestyle in zip(filenames, legends, linestyles):
    actif_key=filename.split('.csv')[0]
    print((actif_key, linestyle))
    dico_actif[actif_key]=[get_actif_data(repository, filename), legend, linestyle]

#%%
pl.figure(1)
pl.clf()
for key in dico_actif:
    data, legend, linestyle = dico_actif[key]
    x_labels, y_acc = data
    pl.plot(x_labels,y_acc,linestyle, label=legend)
    pl.hold(True)
pl.hold(False)
pl.legend(bbox_to_anchor=(0.5, 0.5), loc=2, borderaxespad=0.)
#pl.plot(ytest,yest,'+')
#%%
xl=pl.axis()
#pl.plot([min(xl[0],xl[2]),max(xl[1],xl[3])],[min(xl[0],xl[2]),max(xl[1],xl[3])],'k')
pl.plot(ytest,yest,'+')
pl.plot([0,45],[0,45],'k')
#pl.plot([min(xl[0],xl[2]),max(xl[1],xl[3])],[min(xl[0],xl[2]),max(xl[1],xl[3])],'k')
pl.axis(xl)

pl.xlim([0,45])
pl.ylim([0,45])
pl.xlabel('True Wass. distance')
pl.ylabel('Predicted Wass. distance')
pl.title('True and predicted Wass. distance')
pl.legend(('Exact prediction','Model prediction'))
pl.savefig('imgs/{}_emd_pred_true.png'.format(expe),dpi=300)
pl.savefig('imgs/{}_emd_pred_true.pdf'.format(expe))

