import os, shutil

path = r'D:\LIDC-IDRI'
expected_path = r'D:\LIDC-IDRI_suitable'
for i in os.listdir(path):
    folder = os.path.join(path,i)
    if len(os.listdir(folder)) >= 512:
        exp_folder = os.path.join(expected_path, i)
        for j in os.listdir(folder):
            shutil.copy(os.path.join(folder,j),exp_folder)