from ia01.utils import compte, unique


def est_identique(d1, d2, attributs):
    """Calcule si d1 et d2 sont identiques selon une liste d'attributs

    Paramètres
    ----------
    d1 : dict
        Individu 1 décrit un par dictionnaire
    d2 : dict
        Individu 2 décrit un par dictionnaire
    attributs : list
        Liste des attributs selon lesquels d1 et d2 sont comparés

    Sorties
    -------
    boolean
        True si d1[a] == d2[a] pour tout a dans attributs
    """
    for a in attributs:
        if d1[a] != d2[a]:
            return False
    return True


def groupe(data, attributs):
    """Regroupe les individus partageant les mêmes attributs

    Paramètres
    ----------
    data : list[dict]
        Liste d'individus décrits par un dictionnaire
    attributs : list
        Liste des attributs selon lesquels les individus sont comparés

    Sorties
    -------
    G : list
        Liste contenant pour chaque individu un indice representant son groupe
        Tous les individus du même groupe sont égaux selon les attributs considérés
        Les groupes sont indexés de 1 jusqu'à max(G) et il y a exactement max(G) groupes différents
    """
    n = len(data)
    G = [0] * n
    idx = 1
    for i in range(n):
        if G[i] == 0:  # Nouveau groupe
            G[i] = idx
            for j in range(i + 1, n):
                if est_identique(data[i], data[j], attributs):
                    G[j] = idx
            idx += 1
    return G


def k_anonymite(data, attributs):
    """k-anonymité d'un jeu de données selon une liste d'attributs

    Paramètres
    ----------
    data : list[dict]
        Liste d'individus décrits par un dictionnaire
    attributs : list
        Liste des attributs selon lesquels les individus sont comparés

    Sorties
    -------
    k : int
        k-anonymité de data selon la liste d'attributs
    """
    G = groupe(data, attributs)
    return min(compte(G))


def discret_seuils(X, k):
    """Calcule les seuils de discrétisation de X pour avoir au moins k éléments par interval

    Paramètres
    ----------
    X : list
        Liste de valeurs à discrétiser
    k : int
        Nombre minimal d'élément entre deux seuils consécutifs

    Sorties
    -------
    seuils : list
        Le nombre d'élements de X tels que seuils[i] <= x < seuils[i+1] est supérieur ou égal à k
        Le dernier élément de seuils est float("inf")
    """
    X = sorted(X)
    lim = [X[0]]
    l = X[0]
    count = 1
    for i in range(1, len(X)):
        if count >= k and X[i] > l:  # Nouveau groupe
            l = X[i]
            count = 1
            lim.append(l)
        else:
            count += 1
            if X[i] > l:
                l = X[i]
    if count < k:  # Le dernier seuils ne construit pas un interval suffisant
        lim[-1] = float("inf")
    else:
        lim.append(float("inf"))
    return lim


def discretisation(x, seuils):
    """Discrétise une valeur selon des seuils

    Paramètres
    ----------
    x : float
        Une valeur à discrétiser
    seuils : list
        Seuils de discrétisation

    Sorties
    -------
    i : int
        Indice tel que seuils[i] <= x < seuils[i+1]
    """
    for i in range(len(seuils) - 1):
        if x >= seuils[i] and x < seuils[i + 1]:
            return i


def l_diversite(data, attributs, sensible):
    """l-diversité d'un jeu de données selon une liste d'attributs

    Paramètres
    ----------
    data : list[dict]
        Liste d'individus décrits par un dictionnaire
    attributs : list
        Liste des attributs selon lesquels les individus sont comparés
    sensible :
        Attribut sensible sur lequel calculer la diversité

    Sorties
    -------
    l : int
        l-diversité de data selon la liste d'attributs
    """
    G = groupe(data, attributs)
    div = []
    for g in unique(G):
        dg = [d for i, d in enumerate(data) if G[i] == g]
        S = [d[sensible] for d in dg]
        l = len(unique(S))
        div.append(l)
    return min(div)
