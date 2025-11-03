import pandas as pd
from faker import Faker
import random
import datetime
import os

# --- CÁC THAM SỐ CẤU HÌNH ---
NUM_STUDENTS = 200
SEMESTER_START = datetime.date(2023, 9, 4)
SEMESTER_END = datetime.date(2023, 12, 31)

MIDTERM_START = datetime.date(2023, 10, 16)
MIDTERM_END = datetime.date(2023, 10, 29)
FINAL_START = datetime.date(2023, 12, 11)
FINAL_END = datetime.date(2023, 12, 24)

PERSONA_DISTRIBUTION = {
    'normal': 0.7,
    'at_risk': 0.2,
    'inactive': 0.1
}

# --- NÂNG CẤP: NGÂN HÀNG CÂU MẪU TIẾNG ANH ---
# Các câu này có từ vựng tương tự bộ dữ liệu huấn luyện (IMDb)
SENTENCE_BANK = {
    'positive': [
        "This course is absolutely amazing, I learned so much.",
        "I'm so happy with my exam results, the effort paid off.",
        "The professor is a fantastic and engaging lecturer.",
        "Student life is a wonderful experience.",
        "Feeling great and very motivated today!"
    ],
    'negative': [
        "This assignment is a complete waste of time and terribly boring.",
        "The plot of this lecture makes no sense, it's just bad.",
        "I'm disappointed with my grade, it was an awful performance.",
        "I feel so lonely and isolated from everyone.",
        "This is the worst course I have ever taken."
    ]
}

def get_random_date(start, end):
    delta = end - start
    return start + datetime.timedelta(days=random.randrange(delta.days))

def is_stressful_period(current_date):
    return (MIDTERM_START <= current_date <= MIDTERM_END) or \
           (FINAL_START <= current_date <= FINAL_END)

print("Bắt đầu tạo bộ dữ liệu mô phỏng nâng cao (tiếng Anh)...")
fake = Faker()

students_data = []
personas = random.choices(list(PERSONA_DISTRIBUTION.keys()), weights=PERSONA_DISTRIBUTION.values(), k=NUM_STUDENTS)
for i in range(NUM_STUDENTS):
    students_data.append({'student_id': i + 1, 'persona': personas[i]})
students_df = pd.DataFrame(students_data)
print(f"Đã tạo {NUM_STUDENTS} sinh viên.")

posts_data = []
logins_data = []
current_date = SEMESTER_START
post_id_counter = 1
login_id_counter = 1

while current_date <= SEMESTER_END:
    for _, student in students_df.iterrows():
        student_id = student['student_id']
        persona = student['persona']
        
        post_chance = 0.1
        if persona == 'at_risk': post_chance = 0.25
        if persona == 'inactive': post_chance = 0.01

        if random.random() < post_chance:
            sentiment_prob = 0.1 # 10% cơ hội đăng bài tiêu cực
            if persona == 'at_risk': sentiment_prob = 0.4
            if is_stressful_period(current_date): sentiment_prob += 0.3 # Tăng mạnh vào mùa thi
            
            content = random.choice(SENTENCE_BANK['negative']) if random.random() < sentiment_prob else random.choice(SENTENCE_BANK['positive'])
            
            posts_data.append({
                'post_id': post_id_counter, 'student_id': student_id,
                'content': content, 'created_at': current_date
            })
            post_id_counter += 1

        login_chance = 0.8
        if persona == 'inactive': login_chance = 0.1
        if random.random() < login_chance:
            login_hour = random.randint(8, 23)
            if persona == 'at_risk' and random.random() < 0.3: # 30% khả năng thức khuya
                login_hour = random.choice([0, 1, 2, 3])
            
            login_time = datetime.datetime.combine(current_date, datetime.time(hour=login_hour, minute=random.randint(0, 59)))
            logins_data.append({'login_id': login_id_counter, 'student_id': student_id, 'timestamp': login_time})
            login_id_counter += 1
        
    current_date += datetime.timedelta(days=1)

posts_df = pd.DataFrame(posts_data)
logins_df = pd.DataFrame(logins_data)
print(f"Đã tạo {len(posts_df)} bài đăng và {len(logins_df)} lượt đăng nhập.")

if not os.path.exists('data'): os.makedirs('data')
students_df.to_csv('data/students.csv', index=False)
posts_df.to_csv('data/posts.csv', index=False)
logins_df.to_csv('data/logins.csv', index=False)

print("\nHoàn thành! Dữ liệu mô phỏng mới đã được lưu.")