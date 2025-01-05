import streamlit as st
import requests

# To run the app: streamlit run streamlit_app.py

# Add this at the start of your app
st.set_page_config(
    page_title="Rakket AI",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("Rakket AI - Drill Recommendations")
user_message = st.text_input("Describe your tennis goals or challenges:")

if st.button("Get Recommendations"):
    st.write("Fetching drills...")
    try:
        response = requests.post(
            "https://rakket-ai-app-988708438942.us-central1.run.app/ai-recommend-drills",
            params={"message": user_message},
            headers={"accept": "application/json"},
        )
        if response.status_code == 200:
            st.markdown(response.json().get("response", "No response"))
        else:
            st.error("Error fetching recommendations. Try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")