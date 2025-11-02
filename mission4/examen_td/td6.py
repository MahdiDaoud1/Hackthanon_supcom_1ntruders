from ia01.utils import lecture_csv
from ia01.privacy import k_anonymite,est_identique,discret_seuils,discretisation
import copy
att=["sex", "age", "group"]
data=lecture_csv(".\data\compas-privacy.csv")
for i in att:
    print(k_anonymite(data, [i]))
print(k_anonymite(data, ["age", "group","sex"]))
uni = [1] * len(data)
for i in range(len(data) - 1):
    if uni[i]:
        for j in range(i + 1, len(data)):
            if est_identique(data[i], data[j], ["age", "sex", "group"]):
                uni[i] = 0
                uni[j] = 0
print(sum(uni))
d=dict()
for x in data:
    if x["group"] not in d:
        d[x["group"]]=1
    else:
        d[x["group"]]+=1
for x in data:
    if x["group"] not in ['African-American','Caucasian']:
        x["group"]='Other'
print(k_anonymite(data, [ "group","sex"]))
x=[int(m["age"]) for m in data]
for k in range(400,450,5):
    s=discret_seuils(x, k)
    dd = copy.deepcopy(data)
    for i in range(len(dd)):
        dd[i]["age"] = discretisation(int(dd[i]["age"]), s)
    print(k_anonymite(dd, ["age", "group","sex"]))
