import os, shutil
import numpy as np      

def union(xray_path, ct_path):
    a = []
    for i in os.listdir(xray_path):
        a.append(i)
    # print(a)
    res = []
    for i in os.listdir(ct_path):
        if i in a:
            res.append(i)
    return res

def main():
    git_dts = r"D:\dataset_github"
    my_dts = r"D:\data_asfloat32"
    img_npy = r"D:\img_npy_asfloat32"
    os.mkdir(my_dts)
    U = union(git_dts, img_npy)
    for i in sorted(U):
        print(f"Processing file {i}:..........................")
        new_subfolder = os.path.join(my_dts, i)
        os.mkdir(new_subfolder)
        ct_npy = sorted(os.listdir(os.path.join(git_dts, i)))
        shutil.copy(os.path.join(git_dts, i, ct_npy[0]), new_subfolder)
        shutil.copy(os.path.join(git_dts, i, ct_npy[2]), new_subfolder)
        shutil.copy(os.path.join(git_dts, i, ct_npy[3]), new_subfolder)
        xray_npy = os.listdir(os.path.join(img_npy, i))[0]
        shutil.copy(os.path.join(img_npy, i, xray_npy), new_subfolder)
        print(f"Done file {i}")
    print("All set")
if __name__ == "__main__":
    main()