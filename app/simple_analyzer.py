import pandas as pd

# --- CÁC THAM SỐ CÓ THỂ THAY ĐỔI ---
DATA_FILE_PATH = 'data/posts.csv'
NEGATIVE_KEYWORDS = ['stress', 'buồn', 'cô đơn', 'chán nản', 'khó']
RISK_THRESHOLD = 2 # Nếu sinh viên có từ 2 bài đăng tiêu cực trở lên -> cảnh báo

def analyze_student_sentiments():
    """
    Đọc dữ liệu bài đăng và phân tích cảm xúc dựa trên từ khóa đơn giản.
    Trả về một danh sách các sinh viên có dấu hiệu rủi ro.
    """
    print("Bắt đầu phân tích dữ liệu...")
    
    try:
        posts_df = pd.read_csv(DATA_FILE_PATH)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file dữ liệu tại '{DATA_FILE_PATH}'.")
        print("Vui lòng chạy script 'scripts/data_simulator.py' trước.")
        return

    # Đếm số bài đăng tiêu cực cho mỗi sinh viên
    risky_students = {} # Dùng dictionary để lưu {student_id: count}

    for index, row in posts_df.iterrows():
        student_id = row['student_id']
        content = str(row['content']).lower() # Chuyển về chữ thường để dễ so sánh
        
        # Kiểm tra xem nội dung có chứa từ khóa tiêu cực không
        has_negative_keyword = any(keyword in content for keyword in NEGATIVE_KEYWORDS)
        
        if has_negative_keyword:
            # Nếu có, tăng bộ đếm cho sinh viên đó
            risky_students[student_id] = risky_students.get(student_id, 0) + 1
    
    print("Phân tích hoàn tất. Lọc ra các sinh viên có nguy cơ...")

    # Lọc ra những sinh viên vượt ngưỡng cảnh báo
    students_to_alert = []
    for student_id, count in risky_students.items():
        if count >= RISK_THRESHOLD:
            students_to_alert.append({
                'student_id': student_id,
                'negative_post_count': count
            })

    return students_to_alert

# --- Chạy chương trình chính ---
if __name__ == "__main__":
    alerts = analyze_student_sentiments()
    
    if alerts is not None:
        if not alerts:
            print("\nKhông phát hiện sinh viên nào có dấu hiệu rủi ro.")
        else:
            print(f"\n[CẢNH BÁO] Phát hiện {len(alerts)} sinh viên có dấu hiệu cần quan tâm:")
            # Sắp xếp danh sách để dễ nhìn
            sorted_alerts = sorted(alerts, key=lambda x: x['negative_post_count'], reverse=True)
            for alert in sorted_alerts:
                print(f" - Sinh viên ID: {alert['student_id']}, Số bài đăng tiêu cực: {alert['negative_post_count']}")