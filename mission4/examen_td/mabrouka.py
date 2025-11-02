from ia01.utils import *
from ia01.privacy import *
from ia01.metriques import *
from ia01.majoritaire import *
from ia01.kppv import *
from ia01.evaluation import *
from ia01.arbre import *
data=lecture_csv(".\data\meteo.csv")
xtrain=[[float(x["temperature"]),float(x["rain"]),float(x["wind_speed"]),float(x["relative_humidity"])] for x in data]
w_rain=0.47
w_temp=0.29
w_wind=0.12
w_hum=0.12
loc,sc=norm_param(xtrain) 
xtrain=normalisation(xtrain,loc,sc)
ytrain=[]
for i in range (len(xtrain)):
    score=(
        -w_rain * xtrain[i][1] +
        w_temp * xtrain[i][0] +
        w_wind * xtrain[i][2] -
        w_hum * xtrain[i][3]
    )
    if score>=0.5:
        ytrain.append(1)
    else:
        ytrain.append(0)
k=5
xk,yk = partition_val_croisee(xtrain,ytrain, 5)

prof = list(range(11)) + [float("inf")]
erreur_cv = [0] * len(prof)

for i in range(k):
    X_val, y_val = xk[i], yk[i]
    X_train, y_train = [], []
    for j in range(k):
        if j != i:
            X_train += xk[j]
            y_train += yk[j]
    arbre = arbre_train(X_train, y_train)
    for j, p in enumerate(prof):
        y_pred_val = arbre_pred(X_val, arbre, max_prof=p)
        erreur_cv[j] += taux_erreur(y_val, y_pred_val) / k

for j, p in enumerate(prof):
    print(f"Taux d'erreur pour prof={p} ; e={erreur_cv[j]:.3f}")
bestp_e = argsort(erreur_cv)[0]
print(f"Profondeur optimale : prof = {bestp_e}")
data=lecture_csv(".\data\zaghouan_weather.csv")