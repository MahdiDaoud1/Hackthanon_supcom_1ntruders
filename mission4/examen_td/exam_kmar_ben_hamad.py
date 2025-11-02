from ia01.utils import *
from ia01.privacy import *
from ia01.metriques import *
from ia01.majoritaire import *
from ia01.kppv import *
from ia01.evaluation import *
from ia01.arbre import *
#prob1
data=lecture_csv(".\data\data_train.csv")
data_val=lecture_csv(".\data\data_val.csv")
data_test=lecture_csv(".\data\data_test.csv")
#ex1.1
c1=len([x for x in data if x["y"]=="c1"])
c2=len([x for x in data if x["y"]=="c2"])
c3=len([x for x in data if x["y"]=="c3"])
#1.2
x_train=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data]
y_train=[x["y"] for x in data]

x_val=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data_val]
y_val=[x["y"] for x in data_val]

l=vote_majoritaire(y_train)
y_pred=[l for i in range (len(y_val))]
print(taux_erreur(y_val,y_pred))
#ex1.3
y_pred=kppv(x_val,x_train,y_train,5,2)
print(taux_erreur(y_pred,y_val))
#1.4
x2=[[float(x["x2"])] for x in data]
loc,sc=norm_param(x2)
print(loc,sc)
#1.5
x2n_train=normalisation(x2,loc,sc)
x2n_val=normalisation([[float(x["x2"])] for x in data_val],loc,sc)

x_train=[[x_train[i][0],x2n_train[i][0],x_train[i][2],x_train[i][3]] for i in range (len(x_train))]
x_val=[[x_val[i][0],x2n_val[i][0],x_val[i][2],x_val[i][3]] for i in range (len(x_val))]

y_pred=kppv(x_val,x_train,y_train,5,2)
print(taux_erreur(y_val,y_pred))
#1.6
k=list(range(1,11))
err=[]
for i in k:
    y_pred=kppv(x_val,x_train,y_train,i,2)
    err.append(taux_erreur(y_val,y_pred))
best_k=k[err.index(min(err))]
print(best_k)
#1.7
x_test=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data_test]
y_test=[x["y"] for x in data_test]
x2n_test=normalisation([[float(x["x2"])] for x in data_test],loc,sc)
x_test=[[x_test[i][0],x2n_test[i][0],x_test[i][2],x_test[i][3]] for i in range (len(x_test))]
y_pred=kppv(x_test,x_train,y_train,best_k,2)
print(taux_erreur(y_test,y_pred))
#1.8
data+=data_val
x_t=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data]
y_t=[x["y"] for x in data]
x2=[[float(x["x2"])] for x in data]
loc,sc=norm_param(x2)
x2n_train=normalisation(x2,loc,sc)
x_t=[[x_t[i][0],x2n_train[i][0],x_t[i][2],x_t[i][3]] for i in range (len(x_t))]

X_K, y_K = partition_val_croisee(x_t, y_t, 5)
k=list(range(1,11))
erreur_cv = [0] * len(k)

for i in range(5):
    X_val, y_val = X_K[i], y_K[i]
    X_train, y_train = [], []
    for j in range(5):
        if j != i:
            X_train += X_K[j]
            y_train += y_K[j]
    for j, p in enumerate(k):
        y_pred_val = kppv(X_val,X_train,y_train,p,2)
        erreur_cv[j] += taux_erreur(y_val, y_pred_val) / 5
bestk= argsort(erreur_cv)[0]
print(bestk)
#1.9
y_pred=kppv(x_test,x_t,y_t,bestk,2)
print(taux_erreur(y_test,y_pred))
#fin du prob1
#prob2
data=lecture_csv(".\data\data_train.csv")
data_val=lecture_csv(".\data\data_val.csv")
data_test=lecture_csv(".\data\data_test.csv")
for x in data:
    if x["y"] in ["c2","c3"]:
        x["y"]="c0"
for x in data_val:
    if x["y"] in ["c2","c3"]:
        x["y"]="c0"
for x in data_test:
    if x["y"] in ["c2","c3"]:
        x["y"]="c0"
x_train=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data]
y_train=[x["y"] for x in data]
x_val=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data_val]
y_val=[x["y"] for x in data_val]
x_test=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data_test]
y_test=[x["y"] for x in data_test]
arbre=arbre_train(x_train,y_train)
y_pred=arbre_pred(x_val,arbre,3)

#2.2
prof=list(range(0,11))
err=[]
for j in prof:
    y_pred=arbre_pred(x_val,arbre,j)
    err.append(taux_erreur(y_val,y_pred))
bestp=prof[err.index(min(err))]
#2.3
y_pred=arbre_pred(x_val,arbre,bestp)
pres=precision(y_val,y_pred,"c1")
rap=rappel(y_val,y_pred,"c1")
f1=f_score(y_val,y_pred,"c1")

#2.4
presc=[]
rapp=[]
f1=[]
for j in prof:
    y_pred=arbre_pred(x_val,arbre,j)
    presc.append(precision(y_val,y_pred,"c1"))
    rapp.append(rappel(y_val,y_pred,"c1"))
    f1.append(f_score(y_val,y_pred,"c1"))

bestp_pres=prof[presc.index(max(presc))]
bestp_rap=prof[rapp.index(max(rapp))]
bestp_f1=prof[f1.index(max(f1))]

#2.5
y_pred=arbre_pred(x_test,arbre,bestp_pres)
print(precision(y_test,y_pred,"c1"))
y_pred=arbre_pred(x_test,arbre,bestp_rap)
print(rappel(y_test,y_pred,"c1"))
y_pred=arbre_pred(x_test,arbre,bestp_f1)
print(f_score(y_test,y_pred,"c1"))
#fin du prob2
#prob 3
data=lecture_csv(".\data\data_train.csv")
data_val=lecture_csv(".\data\data_val.csv")
data_test=lecture_csv(".\data\data_test.csv")
x_train=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data]
y_train=[]
for x in data:
    if x["y"] == "c1":
        y_train.append(1)
    elif x["y"] == "c2":
        y_train.append(2)
    else:
        y_train.append(3)
x_val=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data_val]
y_val=[]
for x in data_val:
    if x["y"] == "c1":
        y_val.append(1)
    elif x["y"] == "c2":
        y_val.append(2)
    else:
        y_val.append(3)
x_test=[[float(x["x1"]),float(x["x2"]),float(x["x3"]),float(x["x4"])] for x in data_test]
y_test=[]
for x in data_test:
    if x["y"] == "c1":
        y_test.append(1)
    elif x["y"] == "c2":
        y_test.append(2)
    else:
        y_test.append(3)
arbre=arbre_train(x_train,y_train,True)
y_pred=arbre_pred(x_val,arbre,3)
print(eqm(y_val,y_pred))
prof=list(range(0,11))
err=[]
for j in prof:
    y_pred=arbre_pred(x_val,arbre,j)
    err.append(eqm(y_val,y_pred))
bestp=prof[err.index(min(err))]
#3.3

#fin du prob 3
#prob4
data=lecture_csv(".\data\dorade.csv")
long=[float(x["longueur"]) for x in data]
poids=[float(x["longueur"]) for x in data]
#4.1 calcul
#ex4.2
l=[]
pd=[]
for j in long:
    if j<q1_long:
        l.append(1)
    elif q1_long<=j<m_l:
        l.append(2)
    elif m_l<=j<q3_l:
        l.append(3)
    else:
        l.append(4)

for j in poids:
    if j<q1_poids:
        pd.append(1)
    elif q1_poids<=j<m_p:
        l.append(2)
    elif m_p<=j<q3_p:
        l.append(3)
    else:
        l.append(4)
for i in range (len(data)):
    data[i]["longueur"]=l[i]
    data[i]["poids"]=pd[i]
print(k_anonymite(data, ["longueur"]))
print(k_anonymite(data, ["poids"]))
print(k_anonymite(data, ["espece"]))
print(k_anonymite(data, ["longueur","espece","poids"]))
#4.3
n = len(data)
is_unique = [True] * n
for i in range(n - 1):
    if is_unique[i]:
        for j in range(i + 1, n):
            if est_identique(data[i], data[j], ["longueur","espece","poids"]):
                is_unique[i] = False
                is_unique[j] = False
print(sum(is_unique))
#4.4
data_extra=lecture_csv(".\data\dorade_extra.csv")
long=[float(x["longueur"]) for x in data_extra]
poids=[float(x["longueur"]) for x in data_extra]
l=[]
pd=[]
for j in long:
    if j<q1_long:
        l.append(1)
    elif q1_long<=j<m_l:
        l.append(2)
    elif m_l<=j<q3_l:
        l.append(3)
    else:
        l.append(4)

for j in poids:
    if j<q1_poids:
        pd.append(1)
    elif q1_poids<=j<m_p:
        l.append(2)
    elif m_p<=j<q3_p:
        l.append(3)
    else:
        l.append(4)
for i in range (len(data_extra)):
    data_extra[i]["longueur"]=l[i]
    data_extra[i]["poids"]=pd[i]
data+=data_extra
print(k_anonymite(data, ["longueur","espece","poids"]))









