from ia01.utils import *
from ia01.metriques import *
from ia01.kppv import *
from ia01.majoritaire import *
from ia01.arbre import *

print("==== TD 02 ====")

## Exercice 1.3
# =============
print("\n== Exercice 1.3 ==")

data = lecture_csv("data/dorade.csv")
n = len(data)

X_train, y_train = [], []
for i in range(n):
    X_train.append([float(data[i]["longueur"]), float(data[i]["poids"])])
    y_train.append(data[i]["espece"])

for k in [3, 5, 7]:
    y_pred = kppv(X_train, X_train, y_train, k)
    print("Taux d'erreur pour k =", k, ":", taux_erreur(y_train, y_pred))


## Exercice 1.4
# =============
print("\n== Exercice 1.4 ==")

for k in [1, 200]:
    y_pred = kppv(X_train, X_train, y_train, k)
    print("Taux d'erreurs pour k =", k, ":", taux_erreur(y_train, y_pred))


## Exercice 1.8
# =============
print("\n== Exercice 1.8 ==")

loc1, scale1 = norm_param(X_train, "echelle")
loc2, scale2 = norm_param(X_train, "centre")

X_norm1 = normalisation(X_train, loc1, scale1)
X_norm2 = normalisation(X_train, loc2, scale2)

for k in [3, 5, 7]:
    y_pred = kppv(X_train, X_train, y_train, k)
    y_norm1 = kppv(X_norm1, X_norm1, y_train, k)
    y_norm2 = kppv(X_norm2, X_norm2, y_train, k)
    print(
        "k =",
        k,
        ", sans norme :",
        taux_erreur(y_train, y_pred),
        ", norme 1 :",
        taux_erreur(y_train, y_norm1),
        ", norme 2 :",
        taux_erreur(y_train, y_norm2),
    )

## Exercice 1.9
# =============
print("\n== Exercice 1.9 ==")

data = lecture_csv("data/dorade.csv")

X_train = [[float(d["longueur"])] for d in data]
y_train = [float(d["poids"]) for d in data]

y_pred = [vote_majoritaire(y_train, reg=True)] * len(y_train)
print("REQM pour le vote majoritaire :", reqm(y_train, y_pred))

for k in [3, 5, 7]:
    y_pred = kppv(X_train, X_train, y_train, k, reg=True)
    print("REQM pour k =", k, ":", reqm(y_train, y_pred))

## Exercice 1.10
# ==============
print("\n== Exercice 1.10 ==")

data = lecture_csv("data/dorade.csv")

X_train = [
    [float(d["longueur"])] + ([1, 0] if d["espece"] == "marbree" else [0, 1])
    for d in data
]
y_train = [float(d["poids"]) for d in data]

y_pred = [vote_majoritaire(y_train, reg=True)] * len(y_train)
print("REQM pour le vote majoritaire :", reqm(y_train, y_pred))

for k in [3, 5, 7]:
    y_pred = kppv(X_train, X_train, y_train, k, reg=True)
    print("REQM pour k =", k, ":", reqm(y_train, y_pred))

## Exercice 2.6
# =============
print("\n== Exercice 2.6 ==")

data = lecture_csv("data/dorade.csv")
n = len(data)

X_train, y_train = [], []
for i in range(n):
    X_train.append([float(data[i]["longueur"]), float(data[i]["poids"])])
    y_train.append(data[i]["espece"])

arbre = arbre_train(X_train, y_train)

for p in [2, 5, 10, 20, 30]:
    y_pred = arbre_pred(X_train, arbre, p)
    print("Profondeur max =", p, ":", taux_erreur(y_train, y_pred))
