from ia01.utils import lecture_csv
from ia01.metriques import valeurs_lim
from ia01.utils import est_complet 
from ia01.evaluation import partition_train_val,partition_val_croisee
from ia01.metriques import taux_erreur
from ia01.arbre import arbre_train, arbre_pred
from ia01.utils import argsort
from ia01.metriques import taux_erreur, precision, rappel, f_score, matrice_confusion
data=lecture_csv(".\data\dep_48_filtre.csv")
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
data=[x for x in data if x["classe_consommation_energie"]!= "N" and x["classe_estimation_ges"] != "N"]
data=[x for x in data if x["annee_construction"]!= "0" and x["annee_construction"] != "1"]
s=[float(x["surface_habitable"]) for x in data]
vmi,vmx=valeurs_lim(s)
data=[x for x in data if float(x["surface_habitable"])>=vmi and float(x["surface_habitable"])<=vmx ]
data=[x for x in data if est_complet(x)]
data=[x for x in data if not (x["surface_baies_orientees_nord"]== "0.0" and x["surface_baies_orientees_est_ouest"]== "0.0" and x["surface_baies_orientees_sud"]== "0.0" and x["surface_planchers_hauts_deperditifs"]== "0.0" and x["surface_planchers_bas_deperditifs"]== "0.0" and x["surface_parois_verticales_opaques_deperditives"]== "0.0")]
data=[x for x in data if not (x["consommation_energie"]== "0.0" and x["estimation_ges"]== "0.0")]
data=lecture_csv(".\data\dep_48_clean.csv")
y=[]
for x in data:
    if x['classe_consommation_energie'] in ['F','G'] or  x['classe_estimation_ges'] in ['F','G']:
        y.append(1)
    else:
        y.append(0)
hola=[]
for x in data:
    l=[]
    for s in champs_descr:
        if s =='tr002_type_batiment_libelle':
            if x[s]=='Maison':
                l+=[0,0,1]
            elif x[s]=='Appartement':
                l+=[1,0,0]
            elif x[s] == "Logements collectifs":
                l+=[0,1,0]
        elif s== 'tr001_modele_dpe_type_libelle':
            if x[s]=='Vente':
                l+=[0,0,0,1]
            elif x[s]=='Neuf':
                l+=[0,0,1,0]
            elif x[s]=='Location':
                l+=[0,1,0,0]
            elif x[s] == "Copropriete":
                l+=[1,0,0,0]
        else:
            l.append(float(x[s]))
    hola.append(l)
xt,yt,xv,yv=partition_train_val(hola,y,1/4)
xk,yk=partition_val_croisee(xt,yt)
l=[]
for i in range(5):
    x_train,y_train=[],[]
    x_val=xk[i]
    y_val=yk[i]
    for j in range(5):
        if j !=i:
            x_train= x_train+ xk[j]
    for j in range(5):
        if j !=i:
            y_train= y_train+ yk[j]
    arbre=arbre_train(x_train,y_train)
    yp=arbre_pred(x_val,arbre,5)
    l.append(taux_erreur(y_val, yp))
#print(f"Taux d'erreur pour prof={5} ; e={sum(l)/len(l):.3f}")
xxk, y_K = partition_val_croisee(xt, yt, 5)

prof = list(range(12)) + [float("inf")]
erreur_cv = [0] * len(prof)
prec_cv = [0] * len(prof)
rap_cv = [0] * len(prof)
f_cv = [0] * len(prof)

for i in range(5):
    X_val, y_val = xxk[i], y_K[i]
    X_train, y_train = [], []
    for j in range(5):
        if j != i:
            X_train += xxk[j]
            y_train += y_K[j]
    arbre = arbre_train(X_train, y_train)
    for j, p in enumerate(prof):
        y_pred_val = arbre_pred(X_val, arbre, max_prof=p)
        erreur_cv[j] += taux_erreur(y_val, y_pred_val) / 5
        prec_cv[j] += precision(y_val, y_pred_val, 1) / 5
        rap_cv[j] += rappel(y_val, y_pred_val, 1) / 5
        f_cv[j] += f_score(y_val, y_pred_val, 1) / 5

"""for j, p in enumerate(prof):
    print(
        f"Taux d'erreur pour prof={p} ; e={erreur_cv[j]:.3f} ; p={prec_cv[j]:.3f} ; r={rap_cv[j]:.3f} ; f={f_cv[j]:.3f}"
    )"""
bestp_e = argsort(erreur_cv)[0]
bestp_p = argsort(prec_cv, True)[0]
bestp_r = argsort(rap_cv, True)[0]
bestp_f = argsort(f_cv, True)[0]
"""print(f"Meilleur taux d'erreur : prof = {bestp_e}")
print(f"Meilleure précision : prof = {bestp_p}")
print(f"Meilleur rappel : prof = {bestp_r}")
print(f"Meilleur F1-score : prof = {bestp_f}")"""
arbre = arbre_train(hola, y)

for p in [bestp_e, bestp_p, bestp_r, bestp_f]:
    print(f"Profondeur = {p}")
    y_pred_test = arbre_pred(xv, arbre, max_prof=p)
    print(y_pred_test)
    erreur_test = taux_erreur(yv, y_pred_test)
    mat_conf = matrice_confusion(yt, y_pred_test, [1, 0])
    for i in range(len(mat_conf)):
        print(mat_conf[i])