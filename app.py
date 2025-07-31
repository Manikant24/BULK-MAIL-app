import streamlit as st
import smtplib
import mimetypes
from email.message import EmailMessage

# 🧠 Send email function
def send_email(sender_email, sender_password, subject, body, recipients, attachments):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    msg.set_content(body)

    for file in attachments:
        content = file.read()
        filetype, _ = mimetypes.guess_type(file.name)
        maintype, subtype = filetype.split('/', 1) if filetype else ('application', 'octet-stream')
        msg.add_attachment(content, maintype=maintype, subtype=subtype, filename=file.name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return False

# 🖥 Streamlit UI
st.title("📨 Bulk Email Sender (User Gmail Login)")
st.write("Send emails with your Gmail account and custom attachments.")

# 🧑‍💻 User Input Section
sender_email = st.text_input("📧 Your Gmail Address", placeholder="you@example.com")
sender_password = st.text_input("🔐 App Password (Not your Gmail password)", type="password")
subject = st.text_input("📌 Subject")
body = st.text_area("📝 Email Body")
recipients_input = st.text_area("👥 Recipients (one email per line)")
attachments = st.file_uploader("📎 Upload Attachments", accept_multiple_files=True)

# 📤 Send Button
if st.button("Send Email"):
    recipients = [email.strip() for email in recipients_input.splitlines() if email.strip()]
    if not sender_email or not sender_password or not subject or not body or not recipients:
        st.warning("⚠️ Please fill in all required fields.")
    else:
        success = send_email(sender_email, sender_password, subject, body, recipients, attachments)
        if success:
            st.success(f"✅ Email sent to {len(recipients)} recipient(s) successfully.")
