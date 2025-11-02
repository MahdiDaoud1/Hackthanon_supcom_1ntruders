def partition_train_val(X, y, r=1/5):
    """Partitionne un ensemble X, y en un ensemble train et val.

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    y : list
        Liste des prédictions associées à X
    r : float [0, 1], default = 0.20
        Ratio de (X, y) à mettre dans l'ensemble de validation
        On choisit r tel que r = 1/K avec K un entier

    Sorties
    -------
    X_train, y_train :
        Ensemble d'apprentissage
    X_val, y_val :
        Ensemble de validation
    """
    n = len(X)
    K = round(1 / r)
    X_train, y_train = [], []
    X_val, y_val = [], []
    for i in range(n):
        if i % K == 0:
            X_val.append(X[i])
            y_val.append(y[i])
        else:
            X_train.append(X[i])
            y_train.append(y[i])
    return X_train, y_train, X_val, y_val


def partition_val_croisee(X, y, K=5):
    """Partitionne un ensemble X, y en K sous-ensemble.

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    y : list
        Liste des prédictions associées à X
    K : int, default = 5
        Nombre de partitions

    Sorties
    -------
    X_K, y_K :
        Liste comprenant les K sous-ensembles de X et y
    """    
    n = len(X)
    X_K, y_K = [], []
    for k in range(K):
        X_K.append([])
        y_K.append([])
    for i in range(n):
        X_K[i % K].append(X[i])
        y_K[i % K].append(y[i])
    return X_K, y_K
