import streamlit as st
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

st.title("Custom Email Sending Dashboard")

# Step 1: Upload File
st.subheader("Step 1: Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data", data.head())

# Step 2: Email Details
st.subheader("Step 2: Customize Emails")
email_account = st.text_input("Your Email Address")
smtp_server = st.text_input("SMTP Server Address")
smtp_port = st.number_input("SMTP Port", min_value=1, max_value=65535, value=587)
email_password = st.text_input("Your Email Password", type="password")
subject = st.text_input("Email Subject")
prompt = st.text_area("Email Personalization Prompt (e.g., 'Hi {name}, ...')")

# Send Emails Button
if st.button("Send Emails"):
    if uploaded_file and email_account and subject and prompt:
        files = {"csv_file": uploaded_file}
        data = {
            "email_account": email_account,
            "email_subject": subject,
            "email_body": prompt,
        }

        response = requests.post(f"{API_BASE}/send/", files=files, data=data)
        if response.status_code == 200:
            st.success("Emails sent successfully!")
        else:
            st.error(f"Error sending emails: {response.text}")
    else:
        st.error("Please fill in all fields.")

# Schedule Emails Button
if st.button("Schedule Emails"):
    if uploaded_file and smtp_server and smtp_port and email_account and email_password and subject and prompt:
        files = {"csv_file": uploaded_file}
        data = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "email_account": email_account,
            "email_password": email_password,
            "email_subject": subject,
            "email_body": prompt,
        }

        response = requests.post(f"{API_BASE}/schedule/", files=files, data=data)
        if response.status_code == 200:
            st.success("Emails scheduled successfully!")
        else:
            st.error(f"Error scheduling emails: {response.text}")
    else:
        st.error("Please fill in all fields.")

# Step 3: View Email Status
st.subheader("Step 3: Email Status")
if st.button("View Status"):
    response = requests.get(f"{API_BASE}/status/")
    if response.status_code == 200:
        statuses = response.json()
        if statuses:
            st.write(pd.DataFrame(statuses))
        else:
            st.info("No email statuses available yet.")
    else:
        st.error(f"Error fetching email statuses: {response.text}")
