import os, shutil

def remove_trash_file(path):
    # path = r"D:\LIDC-IDRI"

    for i in os.listdir(path):
        new_path = os.path.join(path,i)
        for j in os.listdir(new_path):
            dicom_size = os.path.getsize(os.path.join(new_path,j))
            if dicom_size < 500000:
                os.remove(os.path.join(new_path,j))

def check_number_of_dicom_files(path):
    count=0
    for i in os.listdir(path):
        subfolder = os.path.join(path,i)
        if len(os.listdir(subfolder)) <=300:
            count += 1
            print(i) 
    print(count)

def take_n_dicom_files(n, path):
    print("Removing wrong folder:..............................")
    shutil.rmtree(r'D:\256(2)')
    exp_path = r'D:\256(2)'
    print("Creating new folder:................................")
    os.mkdir(exp_path)
    for i in os.listdir(path):
        subfolder = os.path.join(path,i)
        new_folder = os.path.join(exp_path, i)
        os.mkdir(new_folder)
        count=0
        print(f"Checking subfolder {i}:................................")
        for j in os.listdir(subfolder):
            if os.path.getsize(os.path.join(subfolder, j)) > 524288:
                count+=1
        if count >= 256:
            print(f"Subfolder {i} is suitable:................................")
            count = 0
            for j in os.listdir(subfolder):
                if os.path.getsize(os.path.join(subfolder, j)) > 524288:
                    count+=1
                else:
                    continue
                if count == 257:
                    break
                shutil.copy(os.path.join(subfolder,j), new_folder)
            print(f"Done subfolder {i}")
        else:
            print(f"Subfolder {i} is not suitable:................................")
def main():
    path = r'D:\suitable2'
    take_n_dicom_files(256, path)

if __name__ == '__main__':
    main()