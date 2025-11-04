import pandas as pd
import random

# Đường dẫn đến các file
STUDENTS_DATA_PATH = 'data/students.csv'
OUTPUT_PATH = 'data/student_profiles.csv'

print("Bắt đầu tạo bộ dữ liệu Hồ sơ Sinh viên...")

try:
    # Tải dữ liệu sinh viên đã có để lấy ID và persona
    students_df = pd.read_csv(STUDENTS_DATA_PATH)
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file {STUDENTS_DATA_PATH}. Vui lòng chạy data_simulator.py trước.")
    exit()

profiles_data = []

for _, student in students_df.iterrows():
    student_id = student['student_id']
    persona = student['persona']
    
    academic_load = ''
    social_support = ''
    final_stress_level = 0
    final_depression_score = 0
    
    # Tạo dữ liệu dựa trên "cá tính"
    if persona == 'at_risk':
        academic_load = random.choices(['High', 'Medium', 'Low'], weights=[0.6, 0.3, 0.1], k=1)[0]
        social_support = random.choices(['Poor', 'Average', 'Good'], weights=[0.6, 0.3, 0.1], k=1)[0]
        final_stress_level = random.randint(3, 5)
        final_depression_score = random.randint(3, 5)
    elif persona == 'normal':
        academic_load = random.choices(['High', 'Medium', 'Low'], weights=[0.1, 0.6, 0.3], k=1)[0]
        social_support = random.choices(['Poor', 'Average', 'Good'], weights=[0.1, 0.3, 0.6], k=1)[0]
        final_stress_level = random.randint(0, 2)
        final_depression_score = random.randint(0, 2)
    else: # persona == 'inactive'
        academic_load = 'Medium'
        social_support = 'Average'
        final_stress_level = random.randint(1, 3)
        final_depression_score = random.randint(1, 3)
        
    profiles_data.append({
        'student_id': student_id,
        'persona': persona,
        'academic_load': academic_load,
        'social_support': social_support,
        'final_stress_level': final_stress_level,
        'final_depression_score': final_depression_score
    })

profiles_df = pd.DataFrame(profiles_data)
profiles_df.to_csv(OUTPUT_PATH, index=False)

print(f"Hoàn thành! Đã tạo và lưu file '{OUTPUT_PATH}' với {len(profiles_df)} hồ sơ.")