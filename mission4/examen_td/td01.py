from ia01.utils import unique, compte, lecture_csv
from ia01.metriques import taux_erreur, eqm, reqm
from ia01.majoritaire import vote_majoritaire


print("==== TD 01 ====")

## Exercice 1.2
# ==============
print("\n== Exercice 1.2 ==")

print(unique([1, 1, 2, 3, 3, 3, 3]))
print(unique(["chat", "chien", "chien", "chat", "chat", "chat"]))


## Exercice 1.3
# ==============
print("\n== Exercice 1.3 ==")

print(compte([1, 1, 2, 3, 3, 3, 3]))
print(compte(["chat", "chien", "chien", "chat", "chat", "chat"]))


## Exercice 1.6
# ==============
print("\n== Exercice 1.6 ==")

data = lecture_csv("data/dorade.csv")
n = len(data)

y_true = []
for i in range(n):
    y_true.append(data[i]["espece"])

y_maj = vote_majoritaire(y_true)

y_pred = []
for i in range(n):
    y_pred.append(y_maj)

print(taux_erreur(y_true, y_pred))


## Exercice 2.5
# =============
print("\n== Exercice 2.5 ==")

data = lecture_csv("data/dorade.csv")
n = len(data)

y_true = []
for i in range(n):
    y_true.append(float(data[i]["poids"]))

y_maj = vote_majoritaire(y_true, reg=True)

y_pred = []
for i in range(n):
    y_pred.append(y_maj)

print(eqm(y_true, y_pred))

## Exercice 2.6
# =============
print("\n== Exercice 2.6 ==")

print(reqm(y_true, y_pred))
