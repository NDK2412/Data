import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models
import os

# Thiết lập các tham số
IMG_HEIGHT = 224  # ResNet50 yêu cầu kích thước ảnh 224x224
IMG_WIDTH = 224
BATCH_SIZE = 32
NUM_CLASSES = 26  # Thay đổi số này theo số dòng gốm trong dataset của bạn
EPOCHS = 10

# Đường dẫn đến dataset (giả sử bạn có thư mục train và test)
train_dir = 'D:\PY_Code\SecondModel\Data\\train'  # Thay bằng đường dẫn thư mục train
test_dir = 'D:\PY_Code\SecondModel\Data\\test'    # Thay bằng đường dẫn thư mục test

# Tạo ImageDataGenerator để tiền xử lý ảnh
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Chuẩn hóa giá trị pixel về [0, 1]
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load dữ liệu từ thư mục
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Tải mô hình ResNet50 (không bao gồm lớp fully connected cuối)
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))

# Đóng băng các layer của ResNet50 để không train lại
base_model.trainable = False

# Thêm các lớp fully connected của riêng bạn
model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(NUM_CLASSES, activation='softmax')  # Số lớp đầu ra
])

# Compile mô hình
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# In tóm tắt mô hình
model.summary()

# Train mô hình
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=test_generator,
    validation_steps=test_generator.samples // BATCH_SIZE
)

# Đánh giá mô hình
test_loss, test_acc = model.evaluate(test_generator)
print(f"Test accuracy: {test_acc}")

# Lưu mô hình
model.save('resnet50_ceramic_model.h5')