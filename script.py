import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set the path to your OAuth 2.0 credentials JSON file
credentials_path = 'C:/Users/Janith/Downloads/json/A.json'

# Initialize the Gmail API client
def initialize_gmail_client(credentials_path):
    try:
        # Load OAuth 2.0 credentials from the JSON file
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/gmail.readonly']
        )

        # Create the Gmail API client
        service = build('gmail', 'v1', credentials=credentials)

        return service

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# List newly arriving emails
def list_new_emails(service):
    try:
        # Perform a search for "new" emails (unread emails)
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No new emails found.')
        else:
            print('New Emails:')
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print(f"Subject: {msg['subject']}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Initialize the Gmail API client
    gmail_service = initialize_gmail_client(credentials_path)

    if gmail_service:
        # List newly arriving emails
        list_new_emails(gmail_service)

if __name__ == '__main__':
    main()
