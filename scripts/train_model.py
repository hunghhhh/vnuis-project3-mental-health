import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib # Dùng để lưu mô hình đã huấn luyện
import os

# --- Tải các tài nguyên cần thiết từ NLTK (chỉ chạy lần đầu) ---
try:
    stopwords.words('english')
except LookupError:
    print("Đang tải tài nguyên 'stopwords' của NLTK...")
    nltk.download('stopwords')

print("Bắt đầu quá trình huấn luyện mô hình AI...")

# 1. Tải và chuẩn bị dữ liệu
# Dữ liệu được ngăn cách bởi dấu tab ('\t') và không có header
data_path = 'data/imdb_labelled.txt'
df = pd.read_csv(data_path, sep='\t', header=None, names=['sentence', 'label'])
print(f"Đã tải {len(df)} câu mẫu để huấn luyện.")

# 2. Tiền xử lý văn bản (Text Preprocessing)
# Loại bỏ các từ dừng (stopwords) - những từ phổ biến không mang nhiều ý nghĩa như 'a', 'the', 'is'...
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # === SỬA LỖI: Đảm bảo đầu vào luôn là string ===
    safe_text = str(text) 
    # Chuyển thành chữ thường và loại bỏ stopwords
    words = safe_text.lower().split()
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

df['cleaned_sentence'] = df['sentence'].apply(preprocess_text)
print("Đã hoàn thành tiền xử lý văn bản.")

# 3. Vector hóa văn bản (Biến chữ thành số)
# TF-IDF là một kỹ thuật phổ biến để biến văn bản thành các vector số mà máy tính có thể hiểu được.
# Nó sẽ gán trọng số cao hơn cho những từ quan trọng.
vectorizer = TfidfVectorizer(max_features=1000) # Chỉ lấy 1000 từ quan trọng nhất
X = vectorizer.fit_transform(df['cleaned_sentence']).toarray()
y = df['label'].values
print("Đã hoàn thành vector hóa văn bản.")

# 4. Chia dữ liệu thành tập huấn luyện (train) và tập kiểm thử (test)
# 80% để huấn luyện, 20% để kiểm tra xem mô hình học tốt đến đâu
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Huấn luyện mô hình Phân loại (Classifier)
# Logistic Regression là một mô hình đơn giản nhưng hiệu quả cho bài toán phân loại văn bản
model = LogisticRegression()
model.fit(X_train, y_train)
print("Đã huấn luyện xong mô hình!")

# 6. Đánh giá mô hình
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nĐộ chính xác của mô hình trên tập kiểm thử: {accuracy * 100:.2f}%")

# 7. Lưu mô hình và vectorizer đã huấn luyện ra file
# Điều này rất quan trọng để chúng ta có thể tái sử dụng mà không cần huấn luyện lại
if not os.path.exists('app/models'):
    os.makedirs('app/models')

joblib.dump(model, 'app/models/sentiment_model.pkl')
joblib.dump(vectorizer, 'app/models/vectorizer.pkl')

print("\nĐã lưu mô hình vào thư mục /app/models:")
print(" - app/models/sentiment_model.pkl")
print(" - app/models/vectorizer.pkl")