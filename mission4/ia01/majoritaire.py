from ia01.utils import unique, compte, moyenne

## TD01
# ==============

def vote_majoritaire(y, reg=False):
    """Applique le vote majoritaire à la y.

    Paramètres
    ----------
    y : list
        Liste des labels pour l'ensemble des données
    reg : bool, default = False
        Indique s'il s'agit d'un problème de régression (True) ou de classification (False)
        Par défaut, on considère qu'il s'agit d'un problème de classification (reg=False)

    Sorties
    -------
    label
        Classification : label le plus représenté dans la liste y
        Regression : moyenne empirique des éléments de y
    """
    if reg:
        return moyenne(y)
    else:
        label = unique(y)
        nombre = compte(y)
        i_max, n_max = -1, -1
        for i in range(len(label)):
            if nombre[i] > n_max:
                n_max = nombre[i]
                i_max = i
        return label[i_max]