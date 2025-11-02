from ia01.utils import *
from ia01.metriques import *
from ia01.evaluation import *
from ia01.arbre import *

print("==== TD 04 ====")

champs_descr = [
    "annee_construction",
    "surface_habitable",
    "nombre_niveaux",
    "surface_baies_orientees_nord",
    "surface_baies_orientees_est_ouest",
    "surface_baies_orientees_sud",
    "surface_planchers_hauts_deperditifs",
    "surface_planchers_bas_deperditifs",
    "surface_parois_verticales_opaques_deperditives",
    "longitude",
    "latitude",
    "tr001_modele_dpe_type_libelle",
    "tr002_type_batiment_libelle",
]

## Exercice 1.1
# =============
print("\n== Exercice 1.1 ==")

data = lecture_csv("data/dep_48_filtre.csv")
data_ = []
for i in range(len(data)):
    if (
        data[i]["classe_consommation_energie"] != "N"
        and data[i]["classe_estimation_ges"] != "N"
    ):
        data_.append(data[i])
data = data_
print(len(data))

## Exercice 1.2
# =============
print("\n== Exercice 1.2 ==")

data_ = []
for i in range(len(data)):
    if int(data[i]["annee_construction"]) > 1:
        data_.append(data[i])
data = data_
print(len(data))

## Exercice 1.6
# =============
print("\n== Exercice 1.6 ==")

surf_hab = []
for i in range(len(data)):
    surf_hab.append(float(data[i]["surface_habitable"]))
s_min, s_max = valeurs_lim(surf_hab)
print(s_min, s_max)

data_ = []
for i in range(len(data)):
    if (
        float(data[i]["surface_habitable"]) >= s_min
        and float(data[i]["surface_habitable"]) <= s_max
    ):
        data_.append(data[i])
data = data_
print(len(data))

## Exercice 1.8
# =============
print("\n== Exercice 1.8 ==")

data_ = []
for i in range(len(data)):
    if est_complet(data[i]):
        data_.append(data[i])
data = data_
print(len(data))

## Exercice 1.9
# =============
print("\n== Exercice 1.9 ==")

data_ = []
for i in range(len(data)):
    if (
        float(data[i]["surface_baies_orientees_nord"])
        + float(data[i]["surface_baies_orientees_est_ouest"])
        + float(data[i]["surface_baies_orientees_sud"])
        + float(data[i]["surface_planchers_hauts_deperditifs"])
        + float(data[i]["surface_planchers_bas_deperditifs"])
        + float(data[i]["surface_parois_verticales_opaques_deperditives"])
        > 0
    ):
        data_.append(data[i])
data = data_
print(len(data))

# Exercice 1.10
# =============
print("\n== Exercice 1.10 ==")

data_ = []
for i in range(len(data)):
    if float(data[i]["consommation_energie"]) + float(data[i]["estimation_ges"]) > 0:
        data_.append(data[i])
data = data_
print(len(data))

## Exercice 2.1
# =============
data = lecture_csv("data/dep_48_clean.csv")

y = []
for d in data:
    if d["classe_estimation_ges"] in ["F", "G"] or d["classe_consommation_energie"] in [
        "F",
        "G",
    ]:
        y.append(1)
    else:
        y.append(0)

## Exercice 2.2
# =============
X = []
for i in range(len(data)):
    X.append([])
    for c in champs_descr:
        dc = data[i][c]
        if c == "tr001_modele_dpe_type_libelle":
            if dc == "Copropriete":
                X[i] += [1, 0, 0, 0]
            elif dc == "Location":
                X[i] += [0, 1, 0, 0]
            elif dc == "Neuf":
                X[i] += [0, 0, 1, 0]
            elif dc == "Vente":
                X[i] += [0, 0, 0, 1]
        elif c == "tr002_type_batiment_libelle":
            if dc == "Appartement":
                X[i] += [1, 0, 0]
            elif dc == "Logements collectifs":
                X[i] += [0, 1, 0]
            elif dc == "Maison":
                X[i] += [0, 0, 1]
        else:
            X[i].append(float(dc))

## Exercice 2.3
# =============
X, y, X_test, y_test = partition_train_val(X, y, 1 / 4)


## Exercice 2.4
# =============
print("\n== Exercice 2.4 ==")

K = 5
X_K, y_K = partition_val_croisee(X, y, K)

prof = list(range(12)) + [float("inf")]
erreur_cv = [0] * len(prof)

for i in range(K):
    X_val, y_val = X_K[i], y_K[i]
    X_train, y_train = [], []
    for j in range(K):
        if j != i:
            X_train += X_K[j]
            y_train += y_K[j]
    arbre = arbre_train(X_train, y_train)
    for j, p in enumerate(prof):
        y_pred_val = arbre_pred(X_val, arbre, max_prof=p)
        erreur_cv[j] += taux_erreur(y_val, y_pred_val) / K

for j, p in enumerate(prof):
    print(f"Taux d'erreur pour prof={p} ; e={erreur_cv[j]:.3f}")
bestp_e = argsort(erreur_cv)[0]
print(f"Profondeur optimale : prof = {bestp_e}")

## Exercice 2.6
# =============
print("\n== Exercice 2.6 ==")

prof = list(range(12)) + [float("inf")]
erreur_cv = [0] * len(prof)
prec_cv = [0] * len(prof)
rap_cv = [0] * len(prof)
f_cv = [0] * len(prof)

for i in range(K):
    X_val, y_val = X_K[i], y_K[i]
    X_train, y_train = [], []
    for j in range(K):
        if j != i:
            X_train += X_K[j]
            y_train += y_K[j]
    arbre = arbre_train(X_train, y_train)
    for j, p in enumerate(prof):
        y_pred_val = arbre_pred(X_val, arbre, max_prof=p)
        erreur_cv[j] += taux_erreur(y_val, y_pred_val) / K
        prec_cv[j] += precision(y_val, y_pred_val, 1) / K
        rap_cv[j] += rappel(y_val, y_pred_val, 1) / K
        f_cv[j] += f_score(y_val, y_pred_val, 1) / K

for j, p in enumerate(prof):
    print(
        f"Taux d'erreur pour prof={p} ; e={erreur_cv[j]:.3f} ; p={prec_cv[j]:.3f} ; r={rap_cv[j]:.3f} ; f={f_cv[j]:.3f}"
    )
    print(
        f"Taux d'erreur pour prof={p} ; e={erreur_cv[j]} ; p={prec_cv[j]} ; r={rap_cv[j]} ; f={f_cv[j]}"
    )
bestp_e = argsort(erreur_cv)[0]
bestp_p = argsort(prec_cv, True)[0]
bestp_r = argsort(rap_cv, True)[0]
bestp_f = argsort(f_cv, True)[0]
print(f"Meilleur taux d'erreur : prof = {bestp_e}")
print(f"Meilleure précision : prof = {bestp_p}")
print(f"Meilleur rappel : prof = {bestp_r}")
print(f"Meilleur F1-score : prof = {bestp_f}")

## Exercice 2.8
# =============
print("\n== Exercice 2.8 ==")

arbre = arbre_train(X, y)

for p in [bestp_e, bestp_p, bestp_r, bestp_f]:
    print(f"Profondeur = {p}")
    y_pred_test = arbre_pred(X_test, arbre, max_prof=p)
    erreur_test = taux_erreur(y_test, y_pred_test)
    mat_conf = matrice_confusion(y_test, y_pred_test, [1, 0])
    for i in range(len(mat_conf)):
        print(mat_conf[i])
