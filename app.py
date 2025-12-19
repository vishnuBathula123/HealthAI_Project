# app.py
import streamlit as st
from utils import (
    get_condition_info,
    suggest_conditions,
    generate_treatment_guidance,
    assess_emergency,
    get_sample_patient_data,
    generate_ai_chat_response
)

st.set_page_config(
    page_title="HealthAI: Intelligent Healthcare Assistant",
    page_icon="⚕️",
    layout="wide"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; padding: 20px; }
    .sidebar { background-color: #e6f2ff; }
    h1 { color: #2c3e50; border-bottom: 2px solid #2980b9; padding-bottom: 10px; }
    .stButton>button { background-color: #2980b9; color: white; }
    .condition-card {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stTextInput>div>div>input { border: 1px solid #2980b9; }
</style>
""", unsafe_allow_html=True)

if 'current_view' not in st.session_state:
    st.session_state.current_view = "Home Page"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
st.sidebar.header("👤 Patient Profile")
name = st.sidebar.text_input("Full Name")
age = st.sidebar.number_input("Age", 0, 120, 30)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
st.sidebar.text_area("Medical History")

# Main Title
st.title("⚕️ HealthAI: Intelligent Healthcare Assistant")
view_options = ["Home Page", "Patient Chat", "Disease Prediction", "Treatment Plans", "Health Analytics"]
current_view = st.radio("Navigation", view_options, horizontal=True, label_visibility="hidden")

# Home Page
if current_view == "Home Page":
    st.subheader("Welcome to Your Health Assistant")
    st.markdown("""
    **How can I help you today?**
    - Chat about your health concerns
    - Check possible conditions based on symptoms
    - Get treatment recommendations
    - Track your health measurements
    """)
    # Removed broken image permanently

# Patient Chat
elif current_view == "Patient Chat":
    st.subheader("HealthAI Chat Assistant")
    if not st.session_state.chat_history:
        st.session_state.chat_history.append({"role": "assistant", "content": "Hello! I'm your HealthAI assistant. How can I help you today?"})

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your health question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            response = generate_ai_chat_response(prompt)
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

# Disease Prediction
elif current_view == "Disease Prediction":
    st.subheader("Symptom Checker")
    symptoms = st.text_area("Describe all your symptoms in detail:", height=150)

    if st.button("Analyze Symptoms"):
        if symptoms:
            emergency = assess_emergency(symptoms)
            if emergency["emergency"]:
                st.error(f"🚨 EMERGENCY: {emergency['message']}")

            conditions = suggest_conditions(symptoms)
            if conditions:
                st.info("Possible conditions based on your symptoms:")
                for condition in conditions[:5]:
                    info = get_condition_info(condition)
                    with st.expander(f"{condition.title()}"):
                        st.markdown(f"**Overview:** {info['overview']}")
                        st.markdown(f"**Common Symptoms:** {', '.join(info['symptoms'][:5])}")
            else:
                st.info("No matching conditions found. Please provide more symptom details.")

# Treatment Plans
elif current_view == "Treatment Plans":
    st.subheader("Treatment Recommendations")
    condition = st.text_input("Enter a medical condition:")
    if st.button("Get Treatment Plan"):
        if condition:
            plan = generate_treatment_guidance(condition)
            st.markdown(plan)

# Health Analytics
elif current_view == "Health Analytics":
    st.subheader("📊 Health Data Analytics")
    df = get_sample_patient_data(30)

    # Show chart
    st.line_chart(df.set_index("Date"))

    # Show last 7 rows with correct formatting (exclude Date from formatting)
    st.markdown("### Recent readings:")
    st.dataframe(
        df.tail(7).style.format({
            "Heart Rate": "{:.1f}",
            "Systolic BP": "{:.1f}",
            "Diastolic BP": "{:.1f}",
            "Blood Glucose": "{:.1f}"
        })
    )

