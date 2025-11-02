import pandas as pd
from faker import Faker
import random
import datetime

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()

# --- CÁC THAM SỐ CÓ THỂ THAY ĐỔI ---
NUM_STUDENTS = 100
NUM_POSTS = 500
START_DATE = datetime.date(2023, 9, 1)
END_DATE = datetime.date(2023, 11, 30)

# Danh sách các câu mẫu
POSITIVE_SENTENCES = [
    "Môn học này thật thú vị!",
    "Mình vừa đạt điểm cao, vui quá.",
    "Cảm ơn thầy cô đã giảng bài rất hay.",
    "Cuộc sống sinh viên thật tuyệt vời.",
    "Hôm nay trời đẹp, mình cảm thấy rất yêu đời."
]

NEGATIVE_SENTENCES = [
    "Mình cảm thấy rất stress với deadline.",
    "Bài tập khó quá, không biết làm sao.",
    "Kết quả thi không như mong đợi, thật buồn.",
    "Cảm thấy cô đơn và lạc lõng.",
    "Chán nản, không có động lực học tập."
]

print("Bắt đầu tạo dữ liệu mô phỏng...")

# 1. Tạo dữ liệu sinh viên
students_data = [{'student_id': i} for i in range(1, NUM_STUDENTS + 1)]
students_df = pd.DataFrame(students_data)
print(f"Đã tạo {len(students_df)} sinh viên.")

# 2. Tạo dữ liệu bài đăng trên diễn đàn
posts_data = []
for _ in range(NUM_POSTS):
    # Chọn ngẫu nhiên một sinh viên
    student_id = random.randint(1, NUM_STUDENTS)
    
    # Chọn ngẫu nhiên cảm xúc (70% tích cực, 30% tiêu cực)
    if random.random() < 0.7:
        content = random.choice(POSITIVE_SENTENCES)
    else:
        content = random.choice(NEGATIVE_SENTENCES)
    
    # Tạo ngày tháng ngẫu nhiên
    time_between_dates = END_DATE - START_DATE
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    post_date = START_DATE + datetime.timedelta(days=random_number_of_days)
    
    posts_data.append({
        'post_id': len(posts_data) + 1,
        'student_id': student_id,
        'content': content,
        'created_at': post_date
    })

posts_df = pd.DataFrame(posts_data)
print(f"Đã tạo {len(posts_df)} bài đăng.")

# 3. Lưu dữ liệu ra file CSV
# Tạo thư mục 'data' nếu chưa có
import os
if not os.path.exists('data'):
    os.makedirs('data')

students_df.to_csv('data/students.csv', index=False)
posts_df.to_csv('data/posts.csv', index=False)

print("\nHoàn thành! Dữ liệu đã được lưu vào thư mục /data")
print(" - data/students.csv")
print(" - data/posts.csv")