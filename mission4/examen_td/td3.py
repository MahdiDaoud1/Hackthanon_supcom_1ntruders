from ia01.utils import lecture_csv
from ia01.kppv import kppv
from ia01.metriques import taux_erreur
from ia01.evaluation import partition_train_val , partition_val_croisee
data=lecture_csv(".\data\dorade.csv")
print(data)
dtest=lecture_csv(".\data\dorade_test.csv")
"""x_train=[[float(x['longueur']), float(x['poids'])] for x in data ]"""
x_test=[[float(x['longueur']), float(x['poids'])] for x in dtest ]
"y_train=[x['espece'] for x in data]"
y_test=[x['espece'] for x in dtest]
"""for k in [1,3,5,7]:
    y_pred= kppv(x_train,x_train,y_train,k)
    print(taux_erreur(y_train,y_pred))
for k in [1,3,5,7]:
    y_pred= kppv(x_test,x_train,y_train,k)
    print(taux_erreur(y_test,y_pred))"""
x=[[float(x['longueur']), float(x['poids'])] for x in data ]
y=[x['espece'] for x in data]
x_train,y_train,x_val,y_val=partition_train_val(x, y)
for k in [1,3,5,7]:
    y_pred= kppv(x_val,x_train,y_train,k)
    print(taux_erreur(y_val,y_pred))
for k in [1,3,5,7]:
    y_pred= kppv(x_test,x_train,y_train,k)
    print(taux_erreur(y_test,y_pred))
xk,yk=partition_val_croisee(x, y)
for o in [1,3,5,7]:
    l=[]
    for i in range(5):
        x_train,y_train=[],[]
        for j in range(5):
            if j !=i:
                x_train= x_train+ xk[j]
        for j in range(5):
            if j !=i:
                y_train= y_train+ yk[j]
        x_val=xk[i]
        y_val=yk[i]
        y_pred= kppv(x_val,x_train,y_train,o)
        l.append(taux_erreur(y_val,y_pred))
    print(sum(l)/len(l))
