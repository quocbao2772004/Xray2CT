import os
import pylidc as pl

# Thiết lập tệp cấu hình pylidc
config_file = r"C:\Users\PC\pylidc.conf"  # Đường dẫn tới tệp cấu hình
dicom_path = r'D:\LIDC-IDRI'  # Đường dẫn tới thư mục chứa file DICOM

# Kiểm tra nếu tệp cấu hình không tồn tại, thì tạo mới
if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        f.write("[paths]\n")
        f.write(f"dicom = {dicom_path}\n")
    print(f"Created config file at: {config_file}")
else:
    # Đọc tệp cấu hình hiện có và kiểm tra xem đã có mục dicom hay chưa
    with open(config_file, 'r') as f:
        config_content = f.read()

    if "dicom" not in config_content:
        # Thêm đường dẫn tới file DICOM nếu chưa tồn tại trong tệp cấu hình
        with open(config_file, 'a') as f:
            f.write(f"\ndicom = {dicom_path}\n")
        print(f"Updated config file with dicom path: {dicom_path}")
    else:
        print(f"Config file already contains dicom path: {dicom_path}")

# Tạo truy vấn tới một bệnh nhân cụ thể (ví dụ: 'LIDC-IDRI-0001')
scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == 'LIDC-IDRI-0201').first()

if scan is None:
    print("Scan not found for patient ID 'LIDC-IDRI-0201'")
else:
    # In ra đường dẫn tới file DICOM
    dicom_files_path = scan.get_path_to_dicom_files()
    print(f"Path to DICOM files: {dicom_files_path}")

# Bạn có thể kiểm tra xem đường dẫn DICOM đã tồn tại và có thể truy cập không
if os.path.exists(dicom_files_path):
    print(f"Directory exists: {dicom_files_path}")
else:
    print(f"Directory does not exist: {dicom_files_path}")
