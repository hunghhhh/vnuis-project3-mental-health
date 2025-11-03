import streamlit as st
import pandas as pd
from simple_analyzer import analyze_student_sentiments_with_ai
import plotly.express as px
import datetime

# --- Cấu hình trang web ---
st.set_page_config(page_title="Dashboard Sức khỏe Tâm lý SV", page_icon="🧠", layout="wide")
st.title("🧠 Dashboard Phân tích Sức khỏe Tâm lý Sinh viên")

# --- Hàm tải dữ liệu ---
@st.cache_data
def load_all_data():
    try:
        kaggle_df = pd.read_csv('data/students_mental_health_survey.csv')
        posts_df = pd.read_csv('data/posts.csv')
        logins_df = pd.read_csv('data/logins.csv')
        return kaggle_df, posts_df, logins_df
    except FileNotFoundError as e:
        st.error(f"Lỗi tải dữ liệu: Không tìm thấy file. Vui lòng kiểm tra lại. Chi tiết: {e}")
        return None, None, None

@st.cache_data
def get_simulation_alerts():
    results = analyze_student_sentiments_with_ai()
    return results if results else []

# Tải dữ liệu
kaggle_df, posts_df, logins_df = load_all_data()

# --- Giao diện Tab ---
tab1, tab2 = st.tabs(["🔬 Phân tích Khảo sát (Kaggle)", "📊 Phân tích Hành vi (Mô phỏng)"])

with tab1:
    st.header("Phân tích Dữ liệu Khảo sát Sức khỏe Tâm lý (từ Kaggle)")
    if kaggle_df is not None:
        st.markdown("Bộ dữ liệu này chứa kết quả khảo sát từ sinh viên...")
        if st.checkbox("Hiển thị dữ liệu thô (Kaggle)"): st.dataframe(kaggle_df)
        st.subheader("Trực quan hóa Phân bổ Dữ liệu")
        col1, col2 = st.columns(2)
        with col1:
            fig_stress = px.histogram(kaggle_df, x='Stress_Level', title="Phân bổ Mức độ Stress")
            st.plotly_chart(fig_stress, use_container_width=True)
        with col2:
            fig_depression = px.histogram(kaggle_df, x='Depression_Score', title="Phân bổ Điểm Trầm cảm")
            st.plotly_chart(fig_depression, use_container_width=True)
        st.subheader("Mối tương quan giữa các Yếu tố")
        fig_corr = px.scatter(kaggle_df, x='Sleep_Quality', y='Stress_Level', title="Chất lượng Giấc ngủ vs. Mức độ Stress")
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("Nhận xét: Có thể thấy xu hướng chung...")

with tab2:
    st.header("Phân tích Hành vi Tương tác (Dữ liệu Mô phỏng)")
    
    if posts_df is not None and logins_df is not None:
        simulation_alerts = get_simulation_alerts()
        st.subheader("Cảnh báo từ Hệ thống AI (Dựa trên Nội dung Bài đăng)")
        num_risky_students = len(simulation_alerts)
        st.metric("Số Sinh viên có Dấu hiệu Cần quan tâm", f"{num_risky_students}")
        if simulation_alerts:
            alert_df = pd.DataFrame(simulation_alerts).sort_values(by='negative_post_count', ascending=False)
            st.dataframe(alert_df)
        else:
            st.success("Hệ thống AI không phát hiện sinh viên nào vượt ngưỡng cảnh báo.")
        
        st.markdown("---")

        # === GIẢI PHÁP THAY THẾ CUỐI CÙNG ===
        st.subheader("Diễn biến Hành vi Thức khuya trong Học kỳ")
        try:
            logins_df['timestamp'] = pd.to_datetime(logins_df['timestamp'])
            logins_df['hour'] = logins_df['timestamp'].dt.hour
            
            late_night_logins = logins_df[(logins_df['hour'] >= 0) & (logins_df['hour'] <= 4)]
            daily_late_logins = late_night_logins.resample('D', on='timestamp').size().rename('Số lượt đăng nhập đêm')
            
            # 1. Vẽ biểu đồ đường chính
            fig_timeline = px.line(daily_late_logins, title="Số lượng Lượt đăng nhập Đêm (0h-4h) hàng ngày")
            
            # 2. Tạo dữ liệu cho các điểm đánh dấu sự kiện
            events_df = pd.DataFrame({
                'date': pd.to_datetime(['2023-10-16', '2023-12-11']),
                'label': ['Bắt đầu Giữa kỳ', 'Bắt đầu Cuối kỳ'],
                'y_pos': [0, 0] # Đặt các điểm ở dưới cùng của biểu đồ
            })
            
            # 3. Thêm các điểm đánh dấu vào biểu đồ
            fig_timeline.add_scatter(
                x=events_df['date'],
                y=events_df['y_pos'],
                mode='markers+text',
                marker=dict(symbol='star', color='red', size=15),
                text=events_df['label'],
                textposition='bottom center',
                name='Sự kiện',
                showlegend=False
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
            st.info("Nhận xét: Số lượng sinh viên thức khuya có xu hướng tăng vọt trong các giai đoạn thi cử.")
        except Exception as e:
            st.error(f"Đã có lỗi khi vẽ biểu đồ diễn biến: {e}")

        # (Phần biểu đồ histogram bên dưới đã ổn định, giữ nguyên)
        st.subheader("Tổng quan Phân bổ Giờ Đăng nhập")
        fig_hours = px.histogram(logins_df, x='hour', title="Phân bổ Lượt đăng nhập theo Giờ trong Ngày", nbins=24)
        st.plotly_chart(fig_hours, use_container_width=True)