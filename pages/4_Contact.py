import streamlit as st


st.set_page_config(
    page_title="Contact",
    page_icon="📞",
    layout="wide"
)

import ui
ui.inject_custom_css()
ui.top_navbar("Contact")

st.title("📞 Contact")

st.write(
    "For project-related information, you can use the "
    "details below."
)


st.divider()


col1, col2 = st.columns(2)


with col1:

    st.subheader("👩‍💻 Project")

    st.write("Insurance Fraud Detection System")

    st.write("Machine Learning Project")

    st.write("Algorithm: Logistic Regression")


with col2:

    st.subheader("🛠️ Technologies")

    st.write("Python")

    st.write("Pandas")

    st.write("Scikit-learn")

    st.write("Streamlit")


st.divider()


st.info(
    "💡 This application is developed as a Machine Learning "
    "project for insurance fraud prediction."
)