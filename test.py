import os
import random
import shutil

# Đường dẫn đến thư mục dataset gốc
dataset_dir = r'D:\PY_Code\SecondModel\Dataset'

# Đường dẫn để lưu file train và test
train_dir = r'D:\PY_Code\SecondModel\Data\train'
test_dir = r'D:\PY_Code\SecondModel\Data\test'

# Tạo thư mục train và test nếu chưa có
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Lấy danh sách tất cả các class (thư mục con trực tiếp trong dataset_dir)
classes = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]

# Danh sách để lưu file train và test
train_files = []
test_files = []

# Duyệt qua từng class
for class_name in classes:
    class_path = os.path.join(dataset_dir, class_name)
    # Lấy danh sách subclass trong class
    subclasses = [d for d in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, d))]

    # Duyệt qua từng subclass để chọn 1 ảnh làm test
    for subclass_name in subclasses:
        subclass_path = os.path.join(class_path, subclass_name)
        # Lấy tất cả file ảnh trong subclass
        image_files = [f for f in os.listdir(subclass_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
        image_files = [os.path.join(subclass_path, f) for f in image_files]

        if len(image_files) == 0:
            print(f"Không tìm thấy ảnh trong subclass {subclass_name} của class {class_name}")
            continue

        # Chọn ngẫu nhiên 1 ảnh làm test từ subclass
        test_image = random.choice(image_files)
        test_files.append(test_image)

        # Các ảnh còn lại trong subclass làm train
        train_images = [img for img in image_files if img != test_image]
        train_files.extend(train_images)

# Copy file test giữ nguyên cấu trúc thư mục
for img in test_files:
    class_name = os.path.basename(os.path.dirname(os.path.dirname(img)))  # Lấy tên class
    subclass_name = os.path.basename(os.path.dirname(img))  # Lấy tên subclass
    target_dir = os.path.join(test_dir, class_name, subclass_name)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(img, os.path.join(target_dir, os.path.basename(img)))

# Copy file train giữ nguyên cấu trúc thư mục
for img in train_files:
    class_name = os.path.basename(os.path.dirname(os.path.dirname(img)))  # Lấy tên class
    subclass_name = os.path.basename(os.path.dirname(img))  # Lấy tên subclass
    target_dir = os.path.join(train_dir, class_name, subclass_name)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(img, os.path.join(target_dir, os.path.basename(img)))

# In số lượng file để kiểm tra
print(f"Tổng số file train: {len(train_files)}")
print(f"Tổng số file test: {len(test_files)} (1 ảnh mỗi subclass)")
print(f"Danh sách class: {classes}")

# In danh sách file
print("\nFile test:")
for f in test_files:
    print(f)
print("\nFile train (mẫu 5 file đầu tiên):")
for f in train_files[:5]:
    print(f)
