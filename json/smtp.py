import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
email_address = "janithtesting@gmail.com"
password = "mgtu dtws uadu dpdo"

# Snort machine's SMTP server information
snort_smtp_server = "snort_machine_ip"
snort_smtp_port = 25  # Change this if necessary

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

                # Forward the email to the Snort machine
                msg = MIMEMultipart()
                msg['From'] = email_address
                msg['To'] = "jhydra7689@gmail.com"  # Change this to your Snort machine's email address
                msg['Subject'] = subject
                msg.attach(MIMEText(email_body, 'plain'))

                try:
                    smtp = smtplib.SMTP(snort_smtp_server, snort_smtp_port)
                    smtp.sendmail(email_address, "jhydra7689@gmail.com", msg.as_string())
                    smtp.quit()
                    print("Email forwarded to Snort machine.")
                except Exception as e:
                    print("Failed to forward the email:", str(e))

                break  # Stop processing after finding the first text/plain part

# Close the mailbox and logout
mail.close()
mail.logout()
