import streamlit as st
import pandas as pd
from simple_analyzer import analyze_student_sentiments_with_ai
import plotly.express as px

st.set_page_config(page_title="Dashboard Sức khỏe Tâm lý SV", page_icon="🧠", layout="wide")
st.title("🧠 Dashboard Phân tích Sức khỏe Tâm lý Sinh viên")

@st.cache_data
def load_kaggle_data():
    try:
        df = pd.read_csv('data/Student Mental health.csv')
        return df
    except FileNotFoundError:
        return None

@st.cache_data
def get_simulation_alerts():
    results = analyze_student_sentiments_with_ai()
    return results if results else []

kaggle_df = load_kaggle_data()
simulation_alerts = get_simulation_alerts()

tab1, tab2 = st.tabs(["🔬 Phân tích Khảo sát (Kaggle)", "🤖 Hệ thống AI Mô phỏng"])

with tab1:
    st.header("Phân tích Dữ liệu Khảo sát Sức khỏe Tâm lý Sinh viên")
    
    if kaggle_df is not None:
        st.markdown("Phân tích bộ dữ liệu 'Mental Health in University Students' từ Kaggle.")
        
        if st.checkbox("Hiển thị dữ liệu thô (Kaggle)"):
            st.dataframe(kaggle_df)

        st.subheader("Trực quan hóa Phân bổ Dữ liệu")
        col1, col2 = st.columns(2)
        with col1:
            # === SỬA LỖI 1: Cập nhật tên cột chính xác ===
            fig_depression = px.histogram(kaggle_df, x='Do you have Depression?', title="Phân bổ Tình trạng Trầm cảm")
            st.plotly_chart(fig_depression, use_container_width=True)
        with col2:
            # === SỬA LỖI 2: Cập nhật tên cột chính xác ===
            fig_anxiety = px.histogram(kaggle_df, x='Do you have Anxiety?', title="Phân bổ Tình trạng Lo âu")
            st.plotly_chart(fig_anxiety, use_container_width=True)

        st.subheader("Mối tương quan giữa Điểm GPA và Sức khỏe Tâm lý")
        # === SỬA LỖI 3: Cập nhật tên cột chính xác ===
        # Dọn dẹp dữ liệu GPA
        # Chuyển đổi cột GPA từ dạng string "3.00 - 3.49" thành số trung bình (3.245)
        def convert_gpa(gpa_range):
            try:
                low, high = map(float, gpa_range.split(' - '))
                return (low + high) / 2
            except:
                return None # Bỏ qua các giá trị không hợp lệ
        
        # Tạo bản sao để tránh lỗi SettingWithCopyWarning
        kaggle_df_cleaned = kaggle_df.copy()
        kaggle_df_cleaned['GPA_Value'] = kaggle_df_cleaned['What is your CGPA?'].apply(convert_gpa)
        kaggle_df_cleaned.dropna(subset=['GPA_Value'], inplace=True) # Xóa các dòng có GPA không hợp lệ

        fig_corr = px.box(kaggle_df_cleaned, x='Do you have Depression?', y='GPA_Value', 
                              title="Phân bổ Điểm GPA theo Tình trạng Trầm cảm")
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("Nhận xét: Biểu đồ hộp cho thấy rằng sinh viên có báo cáo bị trầm cảm ('Yes') có xu hướng có điểm GPA trung bình thấp hơn so với nhóm còn lại ('No').")
        
    else:
        st.error("Lỗi: Không tìm thấy file 'data/Student Mental health.csv'. Vui lòng kiểm tra lại.")

with tab2:
    # (Giữ nguyên code của Tab 2 vì nó đã hoạt động tốt)
    st.header("Hệ thống AI Phân tích Cảm xúc (Mô phỏng)")
    st.markdown("Đây là một hệ thống minh chứng khái niệm (Proof of Concept)...")
    
    num_risky_students = len(simulation_alerts)
    st.metric("Số Sinh viên bị AI gắn cờ (từ dữ liệu mô phỏng)", f"{num_risky_students}")

    if not simulation_alerts:
        st.success("Hệ thống AI không phát hiện sinh viên nào vượt ngưỡng cảnh báo...")
    else:
        alert_df = pd.DataFrame(simulation_alerts)
        st.dataframe(alert_df)
    
    st.info("Lưu ý: Dữ liệu hành vi và hệ thống AI này hoạt động độc lập với dữ liệu khảo sát ở Tab 1.")