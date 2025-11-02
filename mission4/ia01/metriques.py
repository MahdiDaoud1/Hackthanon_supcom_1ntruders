from ia01.utils import moyenne, unique

## TD01
# ==============


def taux_erreur(y_true, y_pred):
    """Taux d'erreur pour un problème de classification

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur

    Sorties
    -------
    err : float [0,1]
        Ratio (entre 0 et 1) d'éléments où y_true et y_pred sont différents.
    """
    n = len(y_true)
    err = 0
    for i in range(n):
        if y_true[i] != y_pred[i]:
            err += 1
    return err / n


def eqm(y_true, y_pred):
    """Erreur quadratique moyenne pour un problème de regression

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites

    Sorties
    -------
    e : float
        Erreur quadratique moyenne
    """
    n = len(y_true)
    err = 0
    for i in range(n):
        err += (y_true[i] - y_pred[i]) ** 2
    return err / n


def reqm(y_true, y_pred):
    """Racine de l'erreur quadratique moyenne pour un problème de regression

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites

    Sorties
    -------
    e : float
        Racine de l'erreur quadratique moyenne
    """
    return eqm(y_true, y_pred) ** 0.5


## TD04
# ==============


def repartition(x, X):
    """Fonction de répartition empirique

    Paramètres
    ----------
    x : float
        Valeur où calculer la fonction de répartition
    X : list
        Liste de valeurs quantitatives

    Sorties
    -------
    F : float
        F correspond au ratio d'élements de la liste X
        dont la valeur est inférieure ou égale à x
    """
    n = len(X)
    F = 0
    for i in range(n):
        if X[i] <= x:
            F = F + 1
    return F / n


def quantile(X, alpha):
    """Quantile empirique

    Paramètres
    ----------
    X : list
        Liste de valeurs quantitatives
    alpha : float [0, 1]
        Ordre alpha sur quantile

    Sorties
    -------
    x : float
        x est le plus petit élément de X tel que F(x) >= alpha
        où F(x) est la fonction de répartition empirique
    """
    qx = []
    for x in X:
        if repartition(x, X) >= alpha:
            qx.append(x)
    return min(qx)


def valeurs_lim(X):
    """Valeurs limites avec la méthode des boîtes à moustaches

    Paramètres
    ----------
    X : list
        Liste de valeurs quantitatives

    Sorties
    -------
    v_min, v_max : float
        v_min : plus petit x de X tel que x >= Q1 - 1.5 * IQR
        v_max : plus grand x de X tel que x <= Q3 + 1.5 * IQR
        où Q1, Q3 sont les premier et troisième quartiles de X :
            Q1 = quantile(X, 0.25), Q3 = quantile(X, 0.75)
        et IQR est l'écart interquartile : Q3 - Q1
    """
    q1 = quantile(X, 0.25)
    q3 = quantile(X, 0.75)
    IQR = q3 - q1
    x_min, x_max = [], []
    for x in X:
        if x >= q1 - 1.5 * IQR:
            x_min.append(x)
        if x <= q3 + 1.5 * IQR:
            x_max.append(x)
    v_min = min(x_min)
    v_max = max(x_max)

    return v_min, v_max


def precision(y_true, y_pred, label_pos):
    """Précision

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur
    label_pos :
        Label de la classe considérée comme positive

    Sorties
    -------
    prec : float [0,1]
        prec = VP / (VP + FP)
        Si VP + FP = 0, alors prec = 0
    """
    VP = 0
    FP = 0
    for i in range(len(y_true)):
        if y_pred[i] == label_pos:
            if y_true[i] == label_pos:
                VP += 1
            else:
                FP += 1
    if VP + FP == 0:
        return 0
    else:
        return VP / (VP + FP)


def rappel(y_true, y_pred, label_pos):
    """Rappel

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur
    label_pos :
        Label de la classe considérée comme positive

    Sorties
    -------
    rap : float [0,1]
        rap = VP / (VP + FN)
        Si VP + FN = 0, alors rap = 0
    """
    VP = 0
    FN = 0
    for i in range(len(y_true)):
        if y_true[i] == label_pos:
            if y_pred[i] == label_pos:
                VP += 1
            else:
                FN += 1
    if VP + FN == 0:
        return 0
    else:
        return VP / (VP + FN)


def f_score(y_true, y_pred, label_pos, beta=1):
    """F-score

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur
    label_pos :
        Label de la classe considérée comme positive
    beta : float, default = 1
        Paramètre beta du score, calcul F1 par défaut

    Sorties
    -------
    f : float [0,1]
        f = ((1 + beta**2)*(prec * rap)) / (beta**2 * prec + rap)
        Si prec = rap = 0, alors f = 0
    """
    prec = precision(y_true, y_pred, label_pos)
    rap = rappel(y_true, y_pred, label_pos)
    if prec + rap == 0:
        return 0
    else:
        return ((1 + beta**2) * (prec * rap)) / (beta**2 * prec + rap)


def matrice_confusion(y_true, y_pred, labels=None):
    """Matrice de confusion

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur
    labels : list
        List des labels du problème de classification

    Sorties
    -------
    mat : list[list]
        Matrice de confusion
        mat[i][j] donne le nombre d'éléments de la classe j ayant
        été prédits comme appartenant à la classe i
    """
    idx = dict(zip(labels, range(len(labels))))
    K = len(labels)
    mat = []
    for k in range(K):
        mat.append([0] * K)
    for yt, yp in zip(y_true, y_pred):
        mat[idx[yp]][idx[yt]] += 1
    return mat


## TD05
# ==============


def TPR(y_true, y_pred, label_pos):
    """Taux de vrais positifs = Rappel

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur
    label_pos :
        Label de la classe considérée comme positive

    Sorties
    -------
    rap : float [0,1]
        rap = VP / (VP + FN)
        Si VP + FN = 0, alors rap = 0
    """
    return rappel(y_true, y_pred, label_pos)


def FPR(y_true, y_pred, label_pos):
    """Taux de faux positifs, False Positive Rate

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur
    label_pos :
        Label de la classe considérée comme positive

    Sorties
    -------
    fpr : float [0,1]
        fpr = FP / (VN + FP)
        Si VN + FP = 0, alors fpr = 0
    """
    FP = 0
    VN = 0
    for i in range(len(y_true)):
        if y_true[i] != label_pos:
            if y_pred[i] == label_pos:
                FP += 1
            else:
                VN += 1
    if FP + VN == 0:
        return 0
    else:
        return FP / (VN + FP)


def ROC(y_true, s_pred, label_pos, seuils):
    """Receiver Operating Characteristic

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    s_pred : list
        Liste contenant les scores de prédiction
    label_pos :
        Label de la classe considérée comme positive
    seuils : list
        Liste de seuils de prédiction, la classe positive est prédite si s_pred >= seuils

    Sorties
    -------
    tpr, fpr : list
        Liste des TPR/FPR pour les différentes valeurs du seuil
    """
    tpr = []
    fpr = []
    for t in seuils:
        y_pred = [label_pos if s >= t else float("nan") for s in s_pred]
        tpr.append(TPR(y_true, y_pred, label_pos))
        fpr.append(FPR(y_true, y_pred, label_pos))
    return tpr, fpr
