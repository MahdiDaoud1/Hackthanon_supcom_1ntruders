from ia01.utils import lecture_csv
from ia01.majoritaire import vote_majoritaire
from ia01.metriques import taux_erreur
from ia01.metriques import eqm
data=lecture_csv(".\data\dorade.csv")
yt=[x["espece"] for x in data]
l=vote_majoritaire(yt)
yf=[l for i in range (len(yt))]
print(data)
print(taux_erreur(yt,yf))
ytt=[float(x["poids"]) for x in data]
print(ytt)
l=vote_majoritaire(ytt,True)
yf=[l for i in range (len(ytt))]
print(eqm(ytt,yf))

