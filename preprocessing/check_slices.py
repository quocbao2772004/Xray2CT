import os, sys
fo = open('file.txt', 'w')
sys.stdout = fo

path = r'D:\LIDC-IDRI-suitable'
a=[]
b=[]
for i in os.listdir(path):
    folder = os.path.join(path,i)
    if len(os.listdir(folder)) >= 500:
        a.append(i)
        b.append(len(os.listdir(folder)))
for i in range(0, len(a)):
    print(a[i])       
# fo.close()
print(len(a))