import configparser
import os

def create_lidc_config(dicom_path):
    # Đường dẫn tới file cấu hình với tên lidc.conf
    config_path = os.path.expanduser(r'F:\project\AI-Medical-Image-Processing\Reconstruction-of-3D-CT-Volume-from-2D-X-ray-Images-using-Deep-Learning\lidc.conf')
    
    # Tạo đối tượng configparser
    config = configparser.ConfigParser()
    
    # Thêm một section và thiết lập đường dẫn DICOM
    config['dicom'] = {'path_to_dicom_files': dicom_path}
    
    # Ghi file cấu hình ra đĩa
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    
    print(f"Config file created at: {config_path}")

if __name__ == "__main__":
    # Thay đường dẫn dưới đây bằng đường dẫn thực tế đến thư mục DICOM của bạn
    dicom_folder_path = r'D:\LIDC-IDRI'
    
    # Gọi hàm để tạo file cấu hình
    create_lidc_config(dicom_folder_path)
