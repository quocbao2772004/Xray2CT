import numpy as np
from scipy.ndimage import zoom
import os

def resized_target(file_path, resized_file_path):
    data = np.load(file_path)
    zoom_factors = (0.5, 0.5, 0.5)  
    resized_data = zoom(data, zoom_factors)
    np.save(resized_file_path, resized_data)
    print(f"shape: {resized_data.shape}")

def resized_drr(file_path, resized_file_path):
    data = np.load(file_path)
    zoom_factors = (0.5, 0.5)  
    resized_data = zoom(data, zoom_factors)
    np.save(resized_file_path, resized_data)
    print(f"shape: {resized_data.shape}")

def main():
    exp_path = r'F:\project\AI-Medical-Image-Processing\Reconstruction-of-3D-CT-Volume-from-2D-X-ray-Images-using-Deep-Learning\resized_folder'
    file_path = r'F:\project\AI-Medical-Image-Processing\Reconstruction-of-3D-CT-Volume-from-2D-X-ray-Images-using-Deep-Learning\aritra_project\dataset1'
    new_path = r'D:\dataset'
    for i in os.listdir(file_path):
        subfolder = os.path.join(file_path, i)
        index = 0
        sub_exp_path = os.path.join(exp_path, i)
        os.mkdir(sub_exp_path)
        for j in sorted(os.listdir(subfolder)):
            npy_file = os.path.join(subfolder, j)
            exp_npy_file = os.path.join(sub_exp_path, j)
            if index == 0:
                resized_target(npy_file, exp_npy_file)
                index = 1
            else:
                resized_drr(npy_file, exp_npy_file)
       
if __name__ =='__main__':
    main()