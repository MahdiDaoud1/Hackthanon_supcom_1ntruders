## TD00
# =============


def test_utils():
    """Fonction de test"""
    print("Test du module utils du package ia01 !")


## TD01
# ==============


def unique(y):
    label = []
    for i in range(len(y)):
        est_dans_label = False
        for j in range(len(label)):
            if y[i] == label[j]:
                est_dans_label = True
                break
        if not est_dans_label:
            label.append(y[i])
    return label


def compte(y):
    label = unique(y)
    K = len(label)
    nombre = [0] * K
    for k in range(K):
        for i in range(len(y)):
            if y[i] == label[k]:
                nombre[k] += 1
    return nombre


def lecture_csv(fichier, sep=","):
    """Lecture d'un fichier texte sous format CSV.
    La première ligne du fichier donne le nom des champs.

    Paramètres
    ----------
    fichier : string
        Chemin vers le fichier à lire
    sep : char, default = ","
        Caractère pour séparer les champs

    Sorties
    -------
    data : list of dict
        Liste des éléments du fichier CSV.
        Chaque élément est stocké dans un dictionnaire dont les champs
        sont donnés par la première ligne du fichier CSV.
    """
    data = []
    with open(fichier, "r") as f:
        lines = f.read().splitlines()
        keys = lines[0].split(sep)
        for line in lines[1:]:
            values = line.split(sep)
            data.append(dict(zip(keys, values)))
    return data


def moyenne(x):
    return sum(x) / len(x)


## TD02
# ==============


def argsort(x, reverse=False):
    """Calcul l'indice de chaque élément dans l'ordre trié.

    Paramètres
    ----------
    x : list
        Liste d'éléments non trié
    reverse : bool
        False (par défaut): tri par ordre croissant
        True : tri par ordre décroissant

    Sorties
    -------
    idx : list
        Liste des indices dans l'ordre
        Si tri croissant, alors x[idx[0]] est le plus petit élément de x
    """
    return sorted(range(len(x)), key=x.__getitem__, reverse=reverse)


def normalisation(X, loc, scale):
    """Méthodes de normalisation de vecteurs

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs sur lesquels appliquer la normalisation
    loc, scale : list
        Liste de paramètres de normalisation pour chaque dimension
        Pour un vecteur x de la liste X, la normalisation pour chaque dimension est :
        x[j] = (x[j] - loc[j]) / scale[j]

    Sorties
    -------
    Xnorm : list[list]
        Liste des vecteurs normalisés
    """
    n = len(X)
    d = len(X[0])
    X_norm = []
    for i in range(n):
        xi_norm = []
        for j in range(d):
            xi_norm.append((X[i][j] - loc[j]) / scale[j])
        X_norm.append(xi_norm)

    return X_norm


def variance(x):
    n = len(x)
    var = 0
    x_moy = moyenne(x)
    for i in range(n):
        var = var + (x[i] - x_moy) ** 2
    var = var / n
    return var


def ecart_type(x):
    return variance(x) ** 0.5


def norm_param(X, methode="echelle"):
    """Calcul des paramètres de normalisation

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partir desquels calculer les paramètres de normalisation
    methode : str, default = "echelle"
        Méthode de normalisation utilisée : "echelle" ou "centre"

    Sorties
    -------
    loc, scale : list
        Liste de paramètres de normalisation pour chaque dimension
    """
    assert (
        methode == "echelle" or methode == "centre"
    ), "Le paramètre `methode` doit valoir `echelle` ou `centre`."

    n = len(X)
    d = len(X[0])
    loc, scale = [], []

    for j in range(d):
        X_j = []
        for i in range(n):
            X_j.append(X[i][j])
        if methode == "echelle":
            min_j = min(X_j)
            max_j = max(X_j)
            loc.append(min_j)
            scale.append(max_j - min_j)
        else:
            moy_j = moyenne(X_j)
            std_j = ecart_type(X_j)
            loc.append(moy_j)
            scale.append(std_j)

    return loc, scale


def gini(y):
    """Calcul de l'impureté de Gini

    Paramètres
    ----------
    y : list
        Liste de labels

    Sorties
    -------
    g : float
        Impureté de Gini
    """
    c = compte(y)
    n = sum(c)
    g = 1
    for ci in c:
        g -= (ci / n) ** 2
    return g

## TD04
# ==============

def est_complet(x):
    """Vérifie que tous les champs de x sont renseignés

    Paramètres
    ----------
    x : dict
        Dictionnaire décrivant une donnée

    Sorties
    -------
    True si tous les champs de x sont différents de la chaîne de caractère vide : ""
    False sinon
    """
    for c in x.keys():
        if x[c] == "":
            return False
    return True