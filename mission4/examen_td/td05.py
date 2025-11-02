from ia01.utils import *
from ia01.metriques import *

print("==== TD 05 ====")

## Exercice 1.1
# =============
print("\n== Exercice 1.1 ==")

data = lecture_csv("data/compas.csv")
data_ = []
for i in range(len(data)):
    if data[i]["race"] == "Caucasian" or data[i]["race"] == "African-American":
        data_.append(data[i])
data = data_
print(len(data))


## Exercice 1.2
# =============
print("\n== Exercice 1.2 ==")

X = [int(d["decile_score"]) for d in data]
G = [1 if d["race"] == "Caucasian" else 2 for d in data]
y_true = [int(d["two_year_recid"]) for d in data]

y_pred = [1 if x >= 8 else 0 for x in X]


## Exercice 1.3
# =============
print("\n== Exercice 1.3 ==")


y1 = [y for y, g in zip(y_pred, G) if g == 1]
y2 = [y for y, g in zip(y_pred, G) if g == 2]

p1 = sum([y for y in y1 if y == 1]) / len(y1)
p2 = sum([y for y in y2 if y == 1]) / len(y2)

print(f"P(y=1|g=1) = {p1*100:.2f}%; P(y=1|g=2) = {p2*100:.2f}%")


## Exercice 1.4
# =============
print("\n== Exercice 1.4 ==")

y1 = [y for y, g in zip(y_pred, G) if g == 1]
y2 = [y for y, g in zip(y_pred, G) if g == 2]
yt1 = [y for y, g in zip(y_true, G) if g == 1]
yt2 = [y for y, g in zip(y_true, G) if g == 2]

tpr1 = TPR(yt1, y1, 1)
fpr1 = FPR(yt1, y1, 1)
tpr2 = TPR(yt2, y2, 1)
fpr2 = FPR(yt2, y2, 1)

print(f"P(y=1|y_true=1, g=1) = {tpr1*100:.2f}%; P(y=1|y_true=0, g=1) = {fpr1*100:.2f}%")
print(f"P(y=1|y_true=1, g=2) = {tpr2*100:.2f}%; P(y=1|y_true=0, g=2) = {fpr2*100:.2f}%")


## Exercice 1.6
# =============
print("\n== Exercice 1.6 ==")

seuils = list(range(1, 12))
X1 = [x for x, g in zip(X, G) if g == 1]
X2 = [x for x, g in zip(X, G) if g == 2]
tpr1, fpr1 = ROC(yt1, X1, 1, seuils)
tpr2, fpr2 = ROC(yt2, X2, 1, seuils)
print(["%.2f" % x for x in tpr1])
print(["%.2f" % x for x in fpr1])
print(["%.2f" % x for x in tpr2])
print(["%.2f" % x for x in fpr2])


## Exercice 1.7
# =============
print("\n== Exercice 1.7 ==")

Diff = []
for i1 in range(len(seuils)):
    diff = []
    for i2 in range(len(seuils)):
        d_tpr = abs(tpr1[i1] - tpr2[i2])
        d_fpr = abs(fpr1[i1] - fpr2[i2])
        d = max(d_tpr, d_fpr)
        diff.append(d)
    Diff.append(diff)

for i in range(len(seuils)):
    print(["%.3f" % x for x in Diff[i]])

for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            print(
                f"t1 = {seuils[i1]}, t2 = {seuils[i2]}, tpr1/tpr2 = {tpr1[i1]:.2f}/{tpr2[i2]:.2f}, fpr1/fpr2 = {fpr1[i1]:.2f}/{fpr2[i2]:.2f}"
            )


## Exercice 1.8
# =============
print("\n== Exercice 1.8 ==")

t1, t2 = None, None
best_f1 = 0
for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            y_pred = []
            for i in range(len(X)):
                if G[i] == 1:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
                else:
                    if X[i] >= seuils[i2]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
            prec = precision(y_true, y_pred, 1)
            rap = rappel(y_true, y_pred, 1)
            f1 = f_score(y_true, y_pred, 1)
            print(f"t1 = {seuils[i1]}, t2 = {seuils[i2]}, prec = {prec:.2f}, rappel = {rap:.2f}, f1 = {f1:.2f}")
            if f1 > best_f1:
                best_f1 = f1
                t1 = seuils[i1]
                t2 = seuils[i2]
print(f"Meilleurs seuils : t1 = {t1}, t2 = {t2}")


## Exercice 1.9
# =============
print("\n== Exercice 1.9 ==")

t1, t2 = None, None
best_f1 = 0
best_prec, best_rec = 0, 0
for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            y_pred = []
            for i in range(len(X)):
                if G[i] == 1:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
                else:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
            f1 = f_score(y_true, y_pred, 1, beta=3)
            if f1 > best_f1:
                best_f1 = f1
                best_prec = precision(y_true, y_pred, 1)
                best_rap = rappel(y_true, y_pred, 1)
                t1 = seuils[i1]
                t2 = seuils[i2]
print(f"Beta = 3, seuils : t1 = {t1}, t2 = {t2}, précision = {best_prec:.3f}, rappel = {best_rap:.3f}")

t1, t2 = None, None
best_f1 = 0
best_prec, best_rec = 0, 0
for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            y_pred = []
            for i in range(len(X)):
                if G[i] == 1:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
                else:
                    if X[i] >= seuils[i2]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
            f1 = f_score(y_true, y_pred, 1, beta=1/3)
            if f1 > best_f1:
                best_f1 = f1
                best_prec = precision(y_true, y_pred, 1)
                best_rap = rappel(y_true, y_pred, 1)
                t1 = seuils[i1]
                t2 = seuils[i2]
print(f"Beta = 1/3, seuils : t1 = {t1}, t2 = {t2}, précision = {best_prec:.3f}, rappel = {best_rap:.3f}")


## Exercice 1.10
# =============
print("\n== Exercice 1.10 ==")

print("Parité démographique")

X = [int(d["decile_score"]) for d in data]
G = [1 if d["sex"] == "Female" else 2 for d in data]
y_true = [int(d["two_year_recid"]) for d in data]

y_pred = [1 if x >= 8 else 0 for x in X]

y1 = [y for y, g in zip(y_pred, G) if g == 1]
y2 = [y for y, g in zip(y_pred, G) if g == 2]

p1 = sum([y for y in y1 if y == 1]) / len(y1)
p2 = sum([y for y in y2 if y == 1]) / len(y2)

print(f"P(y=1|g=1) = {p1*100:.2f}%; P(y=1|g=2) = {p2*100:.2f}%")

print("\nEgalité des chances")

yt1 = [y for y, g in zip(y_true, G) if g == 1]
yt2 = [y for y, g in zip(y_true, G) if g == 2]

tpr1 = TPR(yt1, y1, 1)
fpr1 = FPR(yt1, y1, 1)
tpr2 = TPR(yt2, y2, 1)
fpr2 = FPR(yt2, y2, 1)

print(f"P(y=1|y_true=1, g=1) = {tpr1*100:.2f}%; P(y=1|y_true=0, g=1) = {fpr1*100:.2f}%")
print(f"P(y=1|y_true=1, g=2) = {tpr2*100:.2f}%; P(y=1|y_true=0, g=2) = {fpr2*100:.2f}%")

print("\nSeuils équitables")

seuils = list(range(1, 12))
X1 = [x for x, g in zip(X, G) if g == 1]
X2 = [x for x, g in zip(X, G) if g == 2]
tpr1, fpr1 = ROC(yt1, X1, 1, seuils)
tpr2, fpr2 = ROC(yt2, X2, 1, seuils)

Diff = []
for i1 in range(len(seuils)):
    diff = []
    for i2 in range(len(seuils)):
        d_tpr = abs(tpr1[i1] - tpr2[i2])
        d_fpr = abs(fpr1[i1] - fpr2[i2])
        d = max(d_tpr, d_fpr)
        diff.append(d)
    Diff.append(diff)

for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            print(
                f"t1 = {seuils[i1]}, t2 = {seuils[i2]}, tpr1/tpr2 = {tpr1[i1]:.2f}/{tpr2[i2]:.2f}, fpr1/fpr2 = {fpr1[i1]:.2f}/{fpr2[i2]:.2f}"
            )

t1, t2 = None, None
best_f1 = 0
for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            y_pred = []
            for i in range(len(X)):
                if G[i] == 1:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
                else:
                    if X[i] >= seuils[i2]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
            prec = precision(y_true, y_pred, 1)
            rap = rappel(y_true, y_pred, 1)
            f1 = f_score(y_true, y_pred, 1)
            print(f"t1 = {seuils[i1]}, t2 = {seuils[i2]}, prec = {prec:.2f}, rappel = {rap:.2f}, f1 = {f1:.2f}")
            if f1 > best_f1:
                best_f1 = f1
                t1 = seuils[i1]
                t2 = seuils[i2]
print(f"Meilleurs seuils : t1 = {t1}, t2 = {t2}")

t1, t2 = None, None
best_f1 = 0
best_prec, best_rec = 0, 0
for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            y_pred = []
            for i in range(len(X)):
                if G[i] == 1:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
                else:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
            f1 = f_score(y_true, y_pred, 1, beta=3)
            if f1 > best_f1:
                best_f1 = f1
                best_prec = precision(y_true, y_pred, 1)
                best_rap = rappel(y_true, y_pred, 1)
                t1 = seuils[i1]
                t2 = seuils[i2]
print(f"Beta = 3, seuils : t1 = {t1}, t2 = {t2}, précision = {best_prec:.3f}, rappel = {best_rap:.3f}")

t1, t2 = None, None
best_f1 = 0
best_prec, best_rec = 0, 0
for i1 in range(len(seuils)):
    for i2 in range(len(seuils)):
        if Diff[i1][i2] <= 0.05:
            y_pred = []
            for i in range(len(X)):
                if G[i] == 1:
                    if X[i] >= seuils[i1]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
                else:
                    if X[i] >= seuils[i2]:
                        y_pred.append(1)
                    else:
                        y_pred.append(0)
            f1 = f_score(y_true, y_pred, 1, beta=1/3)
            if f1 > best_f1:
                best_f1 = f1
                best_prec = precision(y_true, y_pred, 1)
                best_rap = rappel(y_true, y_pred, 1)
                t1 = seuils[i1]
                t2 = seuils[i2]
print(f"Beta = 1/3, seuils : t1 = {t1}, t2 = {t2}, précision = {best_prec:.3f}, rappel = {best_rap:.3f}")