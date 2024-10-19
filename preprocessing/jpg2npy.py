import os, cv2
import numpy as np      

def jpg2npy(path, patients, output_folder):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_LINEAR)
    image = (image - np.min(image)) * (1.0 / (np.max(image) - np.min(image)))
    image = image.astype(np.float32)
    os.mkdir(os.path.join(output_folder, patients))
    np.save(os.path.join(output_folder, patients, f"{patients}_drrFrontal.npy"), image)

def main():
    folder = r"F:\project\AI-Medical-Image-Processing\network\images"
    output_folder = r"D:\img_npy_asfloat32"
    os.mkdir(output_folder)
    for i in os.listdir(folder):
        # print(i[: -11])
        jpg2npy(os.path.join(folder,i), i[: -11], output_folder)
   
if __name__ == "__main__":
    main()