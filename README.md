# Đồ án 3: Hệ thống AI & BigData Cảnh báo Sức khỏe Tâm lý Sinh viên


**Sinh viên thực hiện:** Nguyễn Duy Hùng

## Mô tả dự án

Hệ thống xây dựng một dashboard tương tác để phân tích và cảnh báo sớm các dấu hiệu về sức khỏe tâm lý của sinh viên. Dự án sử dụng hai nguồn dữ liệu chính:
1.  **Dữ liệu khảo sát thực tế** từ Kaggle để phân tích các yếu tố nhân khẩu học.
2.  **Dữ liệu hành vi mô phỏng** (lượt đăng nhập, bài đăng) để phân tích các mẫu hình bất thường theo thời gian bằng AI.

## Hướng dẫn Cài đặt và Chạy dự án

### Yêu cầu
- Python 3.8+
- Git

### Các bước cài đặt
1.  Clone repository về máy:
    ```bash
    git clone https://github.com/hunghhhh/vnuis-project3-mental-health.git
    cd vnuis-project3-mental-health
    ```
2.  Tạo và kích hoạt môi trường ảo:
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
3.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
4.  Huấn luyện mô hình AI (chỉ cần chạy lần đầu):
    ```bash
    python scripts/train_model.py
    ```
5.  Chạy dashboard:
    ```bash
    streamlit run app/dashboard.py
    ```