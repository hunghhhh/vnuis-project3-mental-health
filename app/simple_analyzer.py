import pandas as pd
import joblib
import os

# --- ĐƯỜNG DẪN TỚI CÁC FILE ---
DATA_FILE_PATH = 'data/posts.csv'
MODEL_PATH = 'app/models/sentiment_model.pkl'
VECTORIZER_PATH = 'app/models/vectorizer.pkl'

RISK_THRESHOLD = 2 # Ngưỡng cảnh báo: 2 bài đăng tiêu cực trở lên

def analyze_student_sentiments_with_ai():
    """
    Phân tích cảm xúc bài đăng bằng mô hình AI đã được huấn luyện.
    """
    print("Bắt đầu phân tích dữ liệu bằng mô hình AI...")

    # 1. Tải mô hình và vectorizer đã lưu
    try:
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file mô hình AI.")
        print("Vui lòng chạy script 'scripts/train_model.py' trước để huấn luyện mô hình.")
        return

    # 2. Tải dữ liệu bài đăng mô phỏng
    try:
        posts_df = pd.read_csv(DATA_FILE_PATH)
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file dữ liệu tại '{DATA_FILE_PATH}'.")
        print("Vui lòng chạy script 'scripts/data_simulator.py' trước.")
        return

    # 3. Sử dụng mô hình để dự đoán cảm xúc cho từng bài đăng
    # Tiền xử lý và vector hóa nội dung bài đăng
    # Lưu ý: Dữ liệu huấn luyện là tiếng Anh, nhưng logic áp dụng là như nhau.
    # Trong đồ án, ta giả định mô hình đã được huấn luyện với dữ liệu tiếng Việt tương tự.
    post_contents = posts_df['content'].astype(str)
    post_vectors = vectorizer.transform(post_contents)
    
    # Dự đoán (0 = tiêu cực, 1 = tích cực)
    predictions = model.predict(post_vectors)
    posts_df['sentiment_label'] = predictions
    
    print("Đã dự đoán xong cảm xúc cho tất cả bài đăng.")

    # 4. Lọc và đếm các bài đăng tiêu cực (label = 0)
    negative_posts_df = posts_df[posts_df['sentiment_label'] == 0]
    risky_student_counts = negative_posts_df['student_id'].value_counts()
    
    # 5. Lọc ra các sinh viên vượt ngưỡng cảnh báo
    students_to_alert = []
    for student_id, count in risky_student_counts.items():
        if count >= RISK_THRESHOLD:
            students_to_alert.append({
                'student_id': int(student_id),
                'negative_post_count': int(count)
            })

    return students_to_alert

# --- Chạy chương trình chính ---
if __name__ == "__main__":
    alerts = analyze_student_sentiments_with_ai()
    
    if alerts is not None:
        if not alerts:
            print("\nKhông phát hiện sinh viên nào có dấu hiệu rủi ro theo mô hình AI.")
        else:
            print(f"\n[CẢNH BÁO] Mô hình AI phát hiện {len(alerts)} sinh viên có dấu hiệu cần quan tâm:")
            sorted_alerts = sorted(alerts, key=lambda x: x['negative_post_count'], reverse=True)
            for alert in sorted_alerts:
                print(f" - Sinh viên ID: {alert['student_id']}, Số bài đăng tiêu cực: {alert['negative_post_count']}")