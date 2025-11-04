import streamlit as st
import pandas as pd
from simple_analyzer import analyze_student_sentiments_with_ai
import plotly.express as px
import datetime

st.set_page_config(page_title="Student Mental Health Dashboard", page_icon="🧠", layout="wide")
st.title("🧠 Dashboard Phân tích & Cảnh báo Sức khỏe Tâm lý Sinh viên")
st.markdown("Một dự án kết hợp phân tích dữ liệu và AI để phát hiện sớm các dấu hiệu rủi ro về sức khỏe tâm lý.")

@st.cache_data
def load_all_data():
    try:
        kaggle_df = pd.read_csv('data/Student Mental health.csv')
        profiles_df = pd.read_csv('data/student_profiles.csv')
        posts_df = pd.read_csv('data/posts.csv')
        logins_df = pd.read_csv('data/logins.csv')
        return kaggle_df, profiles_df, posts_df, logins_df
    except Exception as e:
        st.error(f"Lỗi tải dữ liệu. Hãy chắc chắn bạn đã tạo đủ các file CSV. Chi tiết: {e}")
        return None, None, None, None

@st.cache_data
def get_simulation_alerts():
    try:
        results = analyze_student_sentiments_with_ai()
        return results if results else []
    except Exception as e:
        st.error(f"Lỗi khi chạy hệ thống AI: {e}")
        return []

kaggle_df_original, profiles_df, posts_df, logins_df = load_all_data()

st.sidebar.header("Bộ lọc Dữ liệu Khảo sát")

if kaggle_df_original is not None:
    course_list = ['Tất cả'] + sorted(list(kaggle_df_original['What is your course?'].unique()))
    gender_list = ['Tất cả'] + sorted(list(kaggle_df_original['Choose your gender'].unique()))
    age_list = ['Tất cả'] + sorted(list(kaggle_df_original['Age'].astype(str).unique()))

    selected_course = st.sidebar.selectbox('Chọn Ngành học:', course_list)
    selected_gender = st.sidebar.selectbox('Chọn Giới tính:', gender_list)
    selected_age = st.sidebar.selectbox('Chọn Tuổi:', age_list)

    kaggle_df_filtered = kaggle_df_original.copy()
    if selected_course != 'Tất cả':
        kaggle_df_filtered = kaggle_df_filtered[kaggle_df_filtered['What is your course?'] == selected_course]
    if selected_gender != 'Tất cả':
        kaggle_df_filtered = kaggle_df_filtered[kaggle_df_filtered['Choose your gender'] == selected_gender]
    if selected_age != 'Tất cả':
        kaggle_df_filtered = kaggle_df_filtered[kaggle_df_filtered['Age'].astype(str) == selected_age]
else:
    kaggle_df_filtered = None

if kaggle_df_filtered is not None and profiles_df is not None and posts_df is not None and logins_df is not None:
    
    st.header("Phần 1: Bằng chứng từ Dữ liệu Khảo sát Thực tế (Kaggle)")
    st.markdown(f"Đang hiển thị dữ liệu cho: **{selected_course}** | **{selected_gender}** | **Tuổi: {selected_age}**")

    with st.expander("Xem Dữ liệu Khảo sát đã lọc"):
        st.dataframe(kaggle_df_filtered)

    def convert_gpa(gpa_range):
        try:
            low, high = map(float, gpa_range.split(' - '))
            return (low + high) / 2
        except: return None
    
    kaggle_df_filtered['GPA_Value'] = kaggle_df_filtered['What is your CGPA?'].apply(convert_gpa)
    kaggle_df_filtered.dropna(subset=['GPA_Value'], inplace=True)
    
    if not kaggle_df_filtered.empty:
        avg_gpa_by_depression = kaggle_df_filtered.groupby('Do you have Depression?')['GPA_Value'].mean().reset_index()
        fig_corr_kaggle = px.bar(
            avg_gpa_by_depression, 
            x='Do you have Depression?', y='GPA_Value', 
            title="So sánh Điểm GPA Trung bình theo Tình trạng Trầm cảm",
            labels={"Do you have Depression?": "Tình trạng Trầm cảm", "GPA_Value": "Điểm GPA Trung bình"},
            color='Do you have Depression?', color_discrete_map={'Yes': 'orange', 'No': 'skyblue'},
            text_auto='.2f', range_y=[3.0, 3.5] 
        )
        st.plotly_chart(fig_corr_kaggle, use_container_width=True)
    else:
        st.warning("Không có dữ liệu phù hợp với bộ lọc đã chọn.")
    
    st.info("=> **Phát hiện 1:** Phân tích cho thấy có sự khác biệt về GPA giữa các nhóm sinh viên khác nhau.")

    st.markdown("---")

    st.header("Phần 2: Phân tích Chuyên sâu các Yếu tố Rủi ro (Dữ liệu Tùy chỉnh)")
    st.markdown("Để hiểu rõ hơn các nguyên nhân tiềm ẩn, chúng ta phân tích bộ dữ liệu hồ sơ sinh viên được mô phỏng chi tiết.")
    load_order = ['Low', 'Medium', 'High']
    profiles_df['academic_load'] = pd.Categorical(profiles_df['academic_load'], categories=load_order, ordered=True)
    avg_stress_grouped = profiles_df.groupby(['academic_load', 'social_support'])['final_stress_level'].mean().reset_index()
    
    # === DÒNG CODE ĐÃ ĐƯỢC SỬA LỖI CÚ PHÁP ===
    fig_corr_custom = px.bar(
        avg_stress_grouped, 
        x='academic_load', 
        y='final_stress_level', 
        color='social_support', 
        barmode='group', 
        title="Mức độ Stress Trung bình theo Áp lực Học tập và Hỗ trợ Xã hội", 
        labels={"academic_load": "Mức độ Áp lực Học tập", "final_stress_level": "Mức độ Stress Trung bình (0-5)", "social_support": "Hỗ trợ Xã hội"}, 
        color_discrete_map={'Good': 'green', 'Average': 'blue', 'Poor': 'red'}
    )
    st.plotly_chart(fig_corr_custom, use_container_width=True)
    st.info("=> **Phát hiện 2:** Áp lực học tập càng cao và thiếu sự hỗ trợ từ xã hội, mức độ stress trung bình càng tăng cao.")

    st.markdown("---")

    st.header("Phần 3: Giải pháp - Giám sát Hành vi & Cảnh báo bằng AI")
    st.markdown("Từ các yếu tố nguy cơ, chúng ta xây dựng hệ thống giám sát các biểu hiện hành vi tương ứng và đưa ra cảnh báo sớm.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Diễn biến Hành vi Thức khuya")
        logins_df['timestamp'] = pd.to_datetime(logins_df['timestamp'])
        logins_df['hour'] = logins_df['timestamp'].dt.hour
        late_night_logins = logins_df[(logins_df['hour'] >= 0) & (logins_df['hour'] <= 4)]
        daily_late_logins = late_night_logins.resample('D', on='timestamp').size().rename('Số lượt đăng nhập đêm')
        fig_timeline = px.line(daily_late_logins, title="Số lượt Đăng nhập Đêm (0h-4h)")
        st.plotly_chart(fig_timeline, use_container_width=True)
    with col2:
        st.subheader("Cảnh báo từ Hệ thống AI")
        alerts = get_simulation_alerts()
        st.metric("Số Sinh viên bị AI gắn cờ", len(alerts))
        if alerts:
            st.dataframe(pd.DataFrame(alerts).sort_values(by='negative_post_count', ascending=False))
        else:
            st.success("Không có cảnh báo mới.")
    st.info("=> **Kết luận:** Hệ thống có khả năng phát hiện các mẫu hành vi bất thường và tự động cảnh báo các trường hợp có nguy cơ.")