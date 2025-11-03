import streamlit as st
import pandas as pd
from simple_analyzer import analyze_student_sentiments_with_ai
import plotly.express as px

# --- Cấu hình trang web ---
st.set_page_config(
    page_title="Hệ thống Cảnh báo Sức khỏe Tâm lý SV",
    page_icon="🧠",
    layout="wide"
)

# --- Tiêu đề Dashboard ---
st.title("🧠 Dashboard Phân tích Sức khỏe Tâm lý Sinh viên")

# --- Hàm tải dữ liệu ---
@st.cache_data
def load_kaggle_data():
    try:
        # === TÊN FILE ĐÃ ĐƯỢỢC CẬP NHẬT CHÍNH XÁC ===
        df = pd.read_csv('data/students_mental_health_survey.csv')
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def get_simulation_alerts():
    results = analyze_student_sentiments_with_ai()
    return results if results else []

# Tải dữ liệu
kaggle_df = load_kaggle_data()
simulation_alerts = get_simulation_alerts()

# --- Giao diện Tab ---
tab1, tab2 = st.tabs(["🔬 Phân tích Khảo sát (Kaggle)", "📊 Phân tích Hành vi (Mô phỏng)"])

# --- NỘI DUNG TAB 1: DỮ LIỆU KAGGLE ---
with tab1:
    st.header("Phân tích Dữ liệu Khảo sát Sức khỏe Tâm lý (từ Kaggle)")
    
    if kaggle_df is not None:
        st.markdown("Bộ dữ liệu này chứa kết quả khảo sát từ sinh viên, cung cấp cái nhìn sâu sắc về các yếu tố ảnh hưởng đến sức khỏe tâm lý.")
        
        # Hiển thị một phần dữ liệu
        if st.checkbox("Hiển thị dữ liệu thô (Kaggle)"):
            st.dataframe(kaggle_df)

        # Vẽ các biểu đồ
        st.subheader("Trực quan hóa Phân bổ Dữ liệu")
        col1, col2 = st.columns(2)
        with col1:
            fig_stress = px.histogram(kaggle_df, x='Stress_Level', title="Phân bổ Mức độ Stress")
            st.plotly_chart(fig_stress, use_container_width=True)
        with col2:
            fig_depression = px.histogram(kaggle_df, x='Depression_Score', title="Phân bổ Điểm Trầm cảm")
            st.plotly_chart(fig_depression, use_container_width=True)

        st.subheader("Mối tương quan giữa các Yếu tố")
        fig_corr = px.scatter(kaggle_df, x='Sleep_Quality', y='Stress_Level', 
                              title="Chất lượng Giấc ngủ vs. Mức độ Stress")
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("Nhận xét: Có thể thấy xu hướng chung, khi chất lượng giấc ngủ (Sleep_Quality) giảm, mức độ stress (Stress_Level) có xu hướng tăng lên.")
        
    else:
        st.error("Lỗi: Không tìm thấy file 'data/students_mental_health_survey.csv'. Vui lòng kiểm tra lại.")

# --- NỘI DUNG TAB 2: DỮ LIỆU MÔ PHỎNG ---
with tab2:
    st.header("Phân tích Hành vi Tương tác (Dữ liệu Mô phỏng)")
    st.markdown("Hệ thống AI phân tích các bài đăng (mô phỏng) để tìm ra sinh viên có nguy cơ dựa trên nội dung văn bản.")
    
    num_risky_students = len(simulation_alerts)
    st.metric("Số Sinh viên có Dấu hiệu Cần quan tâm (từ AI)", f"{num_risky_students}")

    if not simulation_alerts:
        st.success("Hệ thống AI không phát hiện sinh viên nào vượt ngưỡng cảnh báo từ dữ liệu mô phỏng.")
    else:
        alert_df = pd.DataFrame(simulation_alerts)
        st.dataframe(alert_df)

# --- Chân trang ---
st.sidebar.info("Đồ án 3 - hunghhhh")