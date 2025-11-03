import pandas as pd

# Đặt tên file cho dễ nhớ
KAGGLE_DATA_PATH = 'data/students_mental_health_survey.csv' 

# Đặt tên này cho file bạn đã tải về, ví dụ "Student Mental health.csv"
# KAGGLE_DATA_PATH = 'data/Student Mental health.csv' 

print(f"Bắt đầu khám phá file dữ liệu: {KAGGLE_DATA_PATH}")

try:
    # Đọc file CSV vào một DataFrame
    df = pd.read_csv(KAGGLE_DATA_PATH)

    # 1. In ra 5 dòng đầu tiên để xem cấu trúc
    print("\n--- 1. 5 dòng dữ liệu đầu tiên ---")
    print(df.head())

    # 2. In ra thông tin tổng quan (số dòng, số cột, kiểu dữ liệu)
    print("\n--- 2. Thông tin tổng quan (Info) ---")
    df.info()

    # 3. In ra các thống kê mô tả cho các cột số (giá trị trung bình, min, max...)
    print("\n--- 3. Thống kê mô tả (Describe) ---")
    print(df.describe())

    # 4. Đếm số lượng cho một cột cụ thể để xem phân bổ
    print("\n--- 4. Phân bổ Mức độ Stress (Stress_Level) ---")
    print(df['Stress_Level'].value_counts())

    print("\nKhám phá hoàn tất!")

except FileNotFoundError:
    print(f"\nLỖI: Không tìm thấy file tại '{KAGGLE_DATA_PATH}'.")
    print("Hãy chắc chắn rằng bạn đã copy file CSV từ Kaggle vào thư mục /data và tên file khớp với đường dẫn.")