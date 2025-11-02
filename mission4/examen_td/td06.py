from ia01.utils import *
from ia01.privacy import *
import copy

print("==== TD 06 ====")

## Exercice 1.4
# =============
print("\n== Exercice 1.4 ==")

data = lecture_csv("data/compas-privacy.csv")

print(k_anonymite(data, ["sex"]))
print(k_anonymite(data, ["age"]))
print(k_anonymite(data, ["group"]))

n = len(data)
for i in range(n):
    i_unique = True
    for j in range(n):
        if i != j and est_identique(data[i], data[j], ["age"]):
            i_unique = False
            break
    if i_unique:
        print(data[i]["name"], ": age =", data[i]["age"])


## Exercice 1.5
# =============
print("\n== Exercice 1.5 ==")

print(k_anonymite(data, ["sex", "group"]))
print(k_anonymite(data, ["sex", "age"]))
print(k_anonymite(data, ["age", "group"]))

print("\nsex/group :")
n = len(data)
is_unique = [True] * n
for i in range(n - 1):
    if is_unique[i]:
        for j in range(i + 1, n):
            if est_identique(data[i], data[j], ["sex", "group"]):
                is_unique[i] = False
                is_unique[j] = False
    if is_unique[i]:
        print(data[i]["name"], ": sex =", data[i]["sex"], "; group =", data[i]["group"])
print(sum(is_unique))


print("\nsex/age :")
n = len(data)
is_unique = [True] * n
for i in range(n - 1):
    if is_unique[i]:
        for j in range(i + 1, n):
            if est_identique(data[i], data[j], ["age", "sex"]):
                is_unique[i] = False
                is_unique[j] = False
    if is_unique[i]:
        print(data[i]["name"], ": sex =", data[i]["sex"], "; age =", data[i]["age"])
print(sum(is_unique))


print("\nage/group :")
n = len(data)
is_unique = [True] * n
for i in range(n - 1):
    if is_unique[i]:
        for j in range(i + 1, n):
            if est_identique(data[i], data[j], ["age", "group"]):
                is_unique[i] = False
                is_unique[j] = False
    if is_unique[i]:
        print(data[i]["name"], ": age =", data[i]["age"], "; group =", data[i]["group"])
print(sum(is_unique))


## Exercice 1.6
# =============
print("\n== Exercice 1.6 ==")

n = len(data)
is_unique = [True] * n
for i in range(n - 1):
    if is_unique[i]:
        for j in range(i + 1, n):
            if est_identique(data[i], data[j], ["age", "sex", "group"]):
                is_unique[i] = False
                is_unique[j] = False
print(sum(is_unique))


## Exercice 1.7
# =============
print("\n== Exercice 1.7 ==")

group = [d["group"] for d in data]

for gu, gc in zip(unique(group), compte(group)):
    print(gu, ":", gc)


## Exercice 1.8
# =============
print("\n== Exercice 1.8 ==")

for i in range(len(data)):
    if data[i]["group"] in ["Asian", "Native American", "Hispanic"]:
        data[i]["group"] = "Other"

print(k_anonymite(data, ["sex", "group"]))


## Exercice 1.9
# =============
print("\n== Exercice 1.9 ==")

for i in range(len(data)):
    data[i]["age"] = int(data[i]["age"])

for k in range(400, 450, 5):
    seuils = discret_seuils([d["age"] for d in data], k)
    print(seuils)
    dd = copy.deepcopy(data)
    for i in range(len(dd)):
        dd[i]["age"] = discretisation(dd[i]["age"], seuils)
    print(k, k_anonymite(dd, ["sex", "group", "age"]))


## Exercice 2.2
# =============
print("\n== Exercice 2.2 ==")

seuils = [19, 24, 28, 33, float("inf")]

dd = copy.deepcopy(data)
for i in range(len(dd)):
    dd[i]["age"] = discretisation(dd[i]["age"], seuils)

print(l_diversite(dd, ["sex", "group", "age"], "charge"))


## Exercice 2.3
# =============
print("\n== Exercice 2.3 ==")

G = groupe(dd, ["sex", "group", "age"])
for g in unique(G):
    dg = [d for i, d in enumerate(dd) if G[i] == g]
    S = [d["charge"] for d in dg]
    if len(unique(S)) < 4:
        print(unique(S))
        print(dg[0]["sex"], dg[0]["age"], dg[0]["group"])


## Exercice 2.4
# =============
print("\n== Exercice 2.4 ==")
dd.append(
    {"name": "jane doe", "sex": "Female", "age": 2, "group": "Caucasian", "charge": "1"}
)
dd.append(
    {"name": "jane doe", "sex": "Female", "age": 2, "group": "Other", "charge": "4"}
)
dd.append(
    {"name": "jane doe", "sex": "Female", "age": 1, "group": "Caucasian", "charge": "1"}
)
dd.append(
    {"name": "jane doe", "sex": "Female", "age": 0, "group": "Caucasian", "charge": "1"}
)
dd.append(
    {"name": "jane doe", "sex": "Female", "age": 0, "group": "Other", "charge": "1"}
)
dd.append(
    {"name": "jane doe", "sex": "Female", "age": 0, "group": "Other", "charge": "2"}
)
print(l_diversite(dd, ["sex", "group", "age"], "charge"))
