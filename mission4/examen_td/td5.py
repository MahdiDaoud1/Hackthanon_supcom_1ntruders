from ia01.utils import lecture_csv
from ia01.metriques import ROC,f_score,rappel,precision
data=lecture_csv(".\data\compas.csv")
data=[x for x in  data if x["race"] in ["Caucasian","African-American"]]
x=[int(y['decile_score']) for y in data]
g=[]
for  i in data:
    if  i["race"] =="Caucasian":
        g.append(1)
    else:
        g.append(2)
y_true=[int( i['two_year_recid']) for  i in data]
y=[]
for  i in x:
    if  i>=8:
        y.append(1)
    else:
        y.append(0)
vp1=sum([1 for  i in range (len(y)) if y_true[ i] == y[ i] and y[ i]==1 and g[ i] == 1])
fp1=sum([1 for  i in range (len(y)) if y_true[ i] == 0 and  y[ i] == 1 and g[ i] == 1])
fn1=sum([1 for  i in range (len(y)) if y_true[ i] == 1 and y[ i] == 0 and g[ i] == 1])
vn1=sum([1 for  i in range (len(y)) if y_true[ i] == y[ i] and y[ i]==0 and g[ i] == 1])

vp2=sum([1 for  i in range (len(y)) if y_true[ i] == y[ i] and y[ i]==1 and g[ i] == 2])
fp2=sum([1 for  i in range (len(y)) if y_true[ i] == 0 and  y[ i] == 1 and g[ i] == 2])
fn2=sum([1 for  i in range (len(y)) if y_true[ i] == 1 and y[ i] == 0 and g[ i] == 2])
vn2=sum([1 for  i in range (len(y)) if y_true[ i] == y[ i] and y[ i]==0 and g[ i] == 2])
a=(vp1+fp1)/(vp1+fp1+fn1+vn1)
b=(vp2+fp2)/(vp2+fp2+fn2+vn2)
print(a)
print(b)
seuils=[ i for  i in range(1,12)]
x1=[x[ i] for  i in range (len(x)) if g[ i]==1]
x2=[x[ i] for  i in range (len(x)) if g[ i]==2]
y1=[y_true[ i] for  i in range (len(y_true)) if g[ i]==1]
y2=[y_true[ i] for  i in range (len(x)) if g[ i]==2]
tpr1, fpr1 = ROC(y1, x1, 1, seuils)
print(tpr1)
tpr2, fpr2 = ROC(y2, x2, 1, seuils)
print(["%.2f"%x for x in tpr1])
print(fpr1)
print(tpr2)
print(fpr2)
l=[]
for  i in range (len(tpr1)):
    for j in range (len(tpr1)):
        if abs(tpr1[i]-tpr2[j])<=0.05 and abs(fpr1[ i]-fpr2[j])<=0.05:
            l.append(( i+1,j+1))
print(l)
h=[]
for t1,t2 in l:
    y_pred=[]
    for i in range (len(x)):
        if g[i]==1:
            if x[i]>=t1:
                y_pred.append(1)
            else: 
                y_pred.append(0)
        else:
            if x[i]>=t2:
                y_pred.append(1)
            else: 
                y_pred.append(0)

    h.append(f_score(y_true, y_pred, 1,3))
    rappel(y_true, y_pred, 1)
    precision(y_true, y_pred, 1)
print(l[h.index(max(h))])