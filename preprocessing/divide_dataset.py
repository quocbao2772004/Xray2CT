import os, shutil

path = r'D:\data_asfloat32'
# print(len(os.listdir(path)))
dts = r'D:\my_dts_asfloat32'
train = r'D:\my_dts_asfloat32\train'
val = r'D:\my_dts_asfloat32\val'
app = r'D:\my_dts_asfloat32\app'
os.mkdir(dts)
os.mkdir(val)
os.mkdir(train)
os.mkdir(app)
index = 0
total = len(os.listdir(path))
number_train = total * 8 // 10
remain = total - number_train
number_val = remain // 2
number_app = remain - number_val
print(number_train, number_val, number_app)
for i in os.listdir(path):
    folder = os.path.join(path, i)
    index+=1
    if index <= number_train:
        subfolder = os.path.join(train, i)    
    elif index <= number_val:
        subfolder = os.path.join(val, i)   
    else:
        subfolder = os.path.join(app, i)   
    os.mkdir(subfolder)
    shutil.copytree(folder, subfolder, dirs_exist_ok = True)