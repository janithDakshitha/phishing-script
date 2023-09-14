import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText

# Your Gmail credentials
email_address = "your_email@gmail.com"
password = "your_password"

# Snort machine SMTP server configuration
snort_smtp_server = "snort_machine_ip"
snort_smtp_port = 587  # Adjust the port if needed
snort_smtp_username = "your_snort_email@gmail.com"  # Snort machine email address
snort_smtp_password = "your_snort_email_password"

# Connect to Gmail IMAP server
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Log in to your Gmail account
mail.login(email_address, password)

# Select the mailbox you want to read emails from (e.g., "inbox")
mail.select("inbox")

# Search for all unread emails
status, email_ids = mail.search(None, "UNSEEN")

# Convert the email IDs to a list of integers
email_id_list = email_ids[0].split()

# Iterate through the list of email IDs
for email_id in email_id_list:
    # Fetch the email by its ID
    status, msg_data = mail.fetch(email_id, "(RFC822)")

    # Parse the email content
    email_message = email.message_from_bytes(msg_data[0][1])
    
    # Extract email subject
    subject, encoding = decode_header(email_message["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    
    # Extract sender's email address
    sender_email = email.utils.parseaddr(email_message["From"])[1]
    
    # Print email details
    print("Subject:", subject)
    print("From:", sender_email)
    
    # Check if the email has a text/plain payload
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                email_body = part.get_payload(decode=True).decode("utf-8")
                print("\nBody:\n", email_body)
                break  # Stop processing after finding the first text/plain part
    
    # Forward the email to the Snort machine
    msg = MIMEText(email_body)
    msg["Subject"] = subject
    msg["From"] = email_address
    msg["To"] = snort_smtp_username
    
    try:
        smtp = smtplib.SMTP(snort_smtp_server, snort_smtp_port)
        smtp.starttls()
        smtp.login(snort_smtp_username, snort_smtp_password)
        smtp.sendmail(email_address, [snort_smtp_username], msg.as_string())
        smtp.quit()
        print("Email forwarded to Snort machine.")
    except Exception as e:
        print("Failed to forward the email:", e)

# Close the mailbox and logout
mail.close()
mail.logout()
