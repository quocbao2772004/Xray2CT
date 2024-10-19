import os
import numpy as np
import torch, ray
from numba import jit
import albumentations as A

def check_3_dimensional(root):
    # root = r"F:\project\AI-Medical-Image-Processing\Reconstruction-of-3D-CT-Volume-from-2D-X-ray-Images-using-Deep-Learning\aritra_project\dataset1"
    folder = []
    patient_list = [[]for _ in range(len(os.listdir(root)))]
    for i, subfolder in enumerate(os.listdir(root)):
        folder.append(subfolder)
        for j in os.listdir(os.path.join(root, subfolder)):
            patient_list[i].append(j)

    for index in range(0, len(os.listdir(root))):
        inputs = []
        inputs_front = np.load(os.path.join(root, folder[index], patient_list[index][1]))
        inputs_lat = np.load(os.path.join(root, folder[index], patient_list[index][2]))
        inputs_top = np.load(os.path.join(root, folder[index], patient_list[index][3]))
        targets = np.load(os.path.join(root, folder[index], patient_list[index][0]))

        print(inputs_front.shape)
        print(inputs_lat.shape)
        print(inputs_top.shape)
        print(targets.shape)
def check_shape(root):
    input = np.load(root)
    print(input.shape)
@jit(nopython=True, parallel=True)
def generate_drr_from_ct(ct_scan, direction='top'):
    input_shape = ct_scan.shape
    if direction == 'lateral':
        ct_scan = np.transpose(ct_scan, axes=(0, 2, 1))
        input_shape = ct_scan.shape
    elif direction == "frontal":
        ct_scan = np.transpose(ct_scan, axes=(1, 0, 2))
        input_shape = ct_scan.shape

    drr_out = np.zeros((input_shape[0], input_shape[2]), dtype=np.float32)
    for x in range(input_shape[0]):
        for z in range(input_shape[2]):
            u_av = 0.0
            for y in range(input_shape[1]):
                u_av += 0.2 * (ct_scan[x, y, z] + 1000) / (input_shape[1] * 1000)
            drr_out[x, z] = np.exp(0.02 + u_av)
    return drr_out

@ray.remote
def do_full_prprocessing(ct_data):
    drr_front = generate_drr_from_ct(ct_data, direction='frontal')
    drr_lat = generate_drr_from_ct(ct_data, direction='lateral')
    drr_top = generate_drr_from_ct(ct_data, direction='top')

    drr_front = (drr_front - np.min(drr_front)) * (1.0 / (np.max(drr_front) - np.min(drr_front)))
    drr_lat = (drr_lat - np.min(drr_lat)) * (1.0 / (np.max(drr_lat) - np.min(drr_lat)))
    drr_top = (drr_top - np.min(drr_top)) * (1.0 / (np.max(drr_top) - np.min(drr_top)))

    #drr_front = cv2.resize(drr_front, (256, 256), interpolation=cv2.INTER_LINEAR)
    #drr_lat = cv2.resize(drr_lat, (256, 256), interpolation=cv2.INTER_LINEAR)
    #drr_top = cv2.resize(drr_top, (256, 256), interpolation=cv2.INTER_LINEAR)

    return drr_front, drr_lat, drr_top

def check_size_targets(root):
    
    folder = []
    for i in os.listdir(root):
        folder.append(i)
    index = 0
    patient_list = os.listdir(os.path.join(root, folder[index]))
    patient_list.sort()

    ct_dir = os.path.join(root, folder[index], patient_list[0])
    targets = np.load(ct_dir)
    targets = targets.astype('float32')
    print(ct_dir)
    targets = np.transpose(targets, (1, 2, 0))
    aug = A.Compose([
            A.ShiftScaleRotate(shift_limit=0.15, scale_limit=0.15, rotate_limit=45, interpolation=1, border_mode=4, always_apply=False, p=0.3),
            A.RandomCrop(220, 220, always_apply=False, p=1.0),
            A.HorizontalFlip(always_apply=False, p=0.2),
            A.VerticalFlip(always_apply=False, p=0.2),
            A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50, interpolation=1, border_mode=4, always_apply=False, p=0.5),
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, always_apply=False, p=0.2),
            A.MedianBlur(blur_limit=5, always_apply=False, p=0.2),
            A.GaussNoise(var_limit=(10, 50), always_apply=False, p=0.2),
            A.Resize(512, 512),
        ])
    transformed = aug(image=targets, mask=targets)
    targets = transformed['mask']
    targets = (targets - np.min(targets)) * (1.0 / (np.max(targets) - np.min(targets)))
    targets = np.transpose(targets, (2, 0, 1))

    targets_ray = ray.put(targets)

    inputs = ray.get([do_full_prprocessing.remote(targets_ray)])

    inputs = np.asarray(inputs)

    inputs[0][1] = np.rot90(inputs[0][1])
    inputs[0][1] = np.rot90(inputs[0][1])
    inputs[0][1] = np.rot90(inputs[0][1])
    inputs = torch.from_numpy(inputs)
    targets = torch.from_numpy(targets)

def main():
    # os.chdir(r'F:\project\AI-Medical-Image-Processing\Reconstruction-of-3D-CT-Volume-from-2D-X-ray-Images-using-Deep-Learning\aritra_project')
    # root = r'D:\dataset_github'
    # check_3_dimensional(root)
    root = r"D:\img_npy\LIDC-IDRI-0001\LIDC-IDRI-0001_drrFrontal.npy"
    check_shape(root)
    
    root2 = r"D:\dataset\train\LIDC-IDRI-0297\LIDC-IDRI-0297_drrFrontal.npy"
    check_shape(root2)
if __name__ == '__main__':
    
    main()