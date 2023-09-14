import imaplib
import email
from email.header import decode_header
import socket

# Your Gmail credentials
email_address = "janithtesting@gmail.com"
password = "mgtu dtws uadu dpdo"

# Snort machine address and port
snort_machine_ip = "snort_machine_ip"
snort_machine_port = 12345  # Replace with the actual port

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

    # Check if the email has a text/plain payload
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                email_body = part.get_payload(decode=True).decode("utf-8")
                print("Subject:", subject)
                print("From:", sender_email)
                print("Body:\n", email_body)

                # Forward the email content to the Snort machine
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as snort_socket:
                    snort_socket.connect((snort_machine_ip, snort_machine_port))
                    snort_socket.send(f"Subject: {subject}\nFrom: {sender_email}\nBody:\n{email_body}".encode("utf-8"))

                break  # Stop processing after finding the first text/plain part

# Close the mailbox and logout
mail.close()
mail.logout()
