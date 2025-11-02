from ia01.utils import lecture_csv
from ia01.metriques import taux_erreur
from ia01.kppv import kppv
from ia01.utils import norm_param
from ia01.utils import normalisation
from ia01.metriques import reqm
from ia01.arbre import arbre_train, arbre_pred
data=lecture_csv(".\data\dorade.csv")
x_train=[[float(x['longueur']), float(x['poids'])] for x in data ]
y_train=[x['espece'] for x in data]
for k in [1,3,5,7,200]:
    y_pred= kppv(x_train,x_train,y_train,k)
    print(taux_erreur(y_train,y_pred))
l,s=norm_param(x_train,"centre")
x_train=normalisation(x_train,l,s)
for k in [1,3,5,7,200]:
    y_pred= kppv(x_train,x_train,y_train,k)
    print(taux_erreur(y_train,y_pred))
xt=[[float(x["longueur"])] + ([1,0] if x["espece"] == "marbree" else [0,1]) for x in data]
yt=[float(x['poids']) for x in data]
for k in [1,3,5,7,200]:
    yp= kppv(xt,xt,yt,k,2,True)
    print(reqm(yt,yp))
x_train=[[float(x['longueur']), float(x['poids'])] for x in data ]
y_train=[x['espece'] for x in data]
arbre=arbre_train(x_train,y_train)
print(len(y_train))
for p in [2,5,10,20,30]:
    yp=arbre_pred(x_train,arbre,p)
    print(len(yp))
    print("Profondeur max =", p, ":", taux_erreur(y_train, yp))