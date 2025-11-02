from ia01.utils import lecture_csv,est_complet,argsort
from ia01.evaluation import partition_train_val,partition_val_croisee
from ia01.arbre import arbre_train,arbre_pred
from ia01.metriques import taux_erreur
def ecriture_csv_projet(y_pred: list[str], fichier: str = "y_test.csv"):
    assert len(y_pred) == 1923, "Les prédictions doivent contenir 1923 données."
    for y in y_pred:
        assert y in ["Aucun","Faible","Modere","Severe"], "Une prédiction doit avoir une valeur parmi: Aucun, Faible, Modere ou Severe"
    with open(fichier, "w") as f:
        f.write("probleme_sante")
        f.write("\n")
        for y in y_pred:
            f.write(y)
            f.write("\n")
data=lecture_csv(".\data2\X_train.csv")
data_test=lecture_csv(".\data2\X_test.csv")
yt=lecture_csv(".\data2\y_train.csv")

data1=[x for x in data if est_complet(x)]
y_train=[yt[i]["probleme_sante"] for i in range (len(yt)) if est_complet(data[i])]

y_train=[y_train[i] for i in range (len(y_train)) if data1[i]['age']!='0' ]
data1=[x for x in data1 if x['age']!='0']
carac=['age','sexe','cafe_verre','cafeine_mg','sommeil_duree','sommeil_qualite','IMC','rythme_cardiaque','niveau_stress','activite_physique','cigarette','alcool','profession']
x_train=[]
for x in data1:
    l=[]
    for i in carac:
        if i == 'sommeil_qualite':
            if x[i]=='Excellente':
                l.append(4)
            elif x[i]=='Bonne':
                l.append(3)
            elif x[i]=='Passable':
                l.append(2)
            elif x[i] == "Mauvaise":
                l.append(1)
        elif i=='profession':
            if x[i] == "Sante":
                l += [1, 0, 0, 0,0]
            elif x[i] == "Bureau":
                l += [0, 1, 0, 0,0]
            elif x[i] == "Service":
                l += [0, 0, 1, 0,0]
            elif  x[i] == "Etude":
                l += [0, 0, 0, 1,0]
            else:
                l+=[0,0,0,0,1]
        elif i== 'sexe':
            if x[i]== 'Femme':
                l.append(1)
            else:
                l.append(0)
        elif i == 'niveau_stress':
            if x[i]=='Faible':
                l.append(1)
            elif x[i]=='Moyen':
                l.append(2)
            elif x[i] == "Haut":
                l.append(3)
        elif i == 'cigarette':
            if x[i]=='Oui':
                l.append(1)
            else:
                l.append(0)
        elif i == "alcool":
            if x[i]=='Oui':
                l.append(1)
            else:
                l.append(0)
        else:
            l.append(float(x[i]))
    x_train.append(l)
x_t, y_t, x_valf, y_valf = partition_train_val(x_train, y_train, 1 / 5)
arbre_test=arbre_train(x_t,y_t)
k=5
xk,yk = partition_val_croisee(x_t,y_t, 5)

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
y_pred_valf=arbre_pred(x_valf,arbre_test,bestp_e)
print(taux_erreur(y_valf,y_pred_valf))
x_test=[]
for x in data_test:
    l=[]
    for i in carac:
        if i == 'sommeil_qualite':
            if x[i]=='Excellente':
                l.append(4)
            elif x[i]=='Bonne':
                l.append(3)
            elif x[i]=='Passable':
                l.append(2)
            elif x[i] == "Mauvaise":
                l.append(1)
        elif i=='profession':
            if x[i] == "Sante":
                l += [1, 0, 0, 0,0]
            elif x[i] == "Bureau":
                l += [0, 1, 0, 0,0]
            elif x[i] == "Service":
                l += [0, 0, 1, 0,0]
            elif  x[i] == "Etude":
                l += [0, 0, 0, 1,0]
            else:
                l+=[0,0,0,0,1]
        elif i== 'sexe':
            if x[i]== 'Femme':
                l.append(1)
            else:
                l.append(0)
        elif i == 'niveau_stress':
            if x[i]=='Faible':
                l.append(1)
            elif x[i]=='Moyen':
                l.append(2)
            elif x[i] == "Haut":
                l.append(3)
        elif i == 'cigarette':
            if x[i]=='Oui':
                l.append(1)
            else:
                l.append(0)
        elif i == "alcool":
            if x[i]=='Oui':
                l.append(1)
            else:
                l.append(0)
        else:
            l.append(float(x[i]))
    x_test.append(l)
y_pred=arbre_pred(x_test,arbre_test,bestp_e)
ecriture_csv_projet(y_pred)