import imaplib
import email
from email.header import decode_header
import os

# Your Gmail credentials
email_address = "janithtesting@gmail.com"
password = "mgtu dtws uadu dpdo"

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

# Create a named pipe for Snort
snort_pipe_path = "/path/snort_pipe"  # Replace with the actual path
snort_pipe = open(snort_pipe_path, "w")

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

    # Construct a message to send to Snort
    message = f"Subject: {subject}\nFrom: {sender_email}\n\n"

    # Write the message to the named pipe
    snort_pipe.write(message)

# Close the named pipe and file
snort_pipe.close()

# Close the mailbox and logout
mail.close()
mail.logout()
