import os
import shutil, glob

def get_largest_subfolder(base_folder):
    max_size = 0
    largest_subfolder = None

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        if os.path.isdir(folder_path):

            folder_size = sum(
                os.path.getsize(os.path.join(root, file))
                for root, _, files in os.walk(folder_path)
                for file in files
            )

            if folder_size > max_size:
                max_size = folder_size
                largest_subfolder = folder_path

    return largest_subfolder

def main():
    index = 0
    path = r"C:\Users\PC\Downloads\LIDC-IDRI\LIDC-IDRI"
    exp_path = r"D:\New folder"
    for i in sorted(os.listdir(path)):
        subfolder = os.path.join(path, i)
        largest_folder = get_largest_subfolder(subfolder)
        print(f"Processing folder{i}:")
        folders =[]
        for f in sorted(os.listdir(largest_folder)):
            if f.find("Segmentation") == -1 and f.find("Nodule") == -1 and f.find("dcm") == -1:
                folders.append(f)
        # print(folders[0], len(os.listdir(os.path.join(largest_folder, folders[0]))))
        largest_folder = os.path.join(largest_folder, folders[0])
        if len(os.listdir(largest_folder)) >= 256:
            count=0
            for j in os.listdir(largest_folder):
                if os.path.getsize(os.path.join(largest_folder, j)) >= 512000:
                    count+=1
            print(f"Folder{i} has {count} files are suitable")
            if count >= 256:
                new_folder = os.path.join(exp_path, i)
                os.mkdir(new_folder)
                shutil.copytree(largest_folder, new_folder, dirs_exist_ok = True)
if __name__ == '__main__':
    main()