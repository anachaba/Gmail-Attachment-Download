import imaplib
import email
import os

def download_email_attachments(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    
    # Search for emails between 1st February 2023 and 9th February 2023
    result, data = mail.search(None, 'SINCE "31-JAN-2023" BEFORE "7-FEB-2023"')
    
    # Get the list of email IDs
    email_ids = data[0].split()
    
    # Iterate through the list of email IDs
    for email_id in email_ids:
        result, data = mail.fetch(email_id, "(RFC822)")
        email_body = data[0][1]
        email_message = email.message_from_bytes(email_body)
        
        # Get the list of attachments
        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            file_name = part.get_filename()
            if bool(file_name):
                file_path = os.path.join("attachments", file_name)
                with open(file_path, "wb") as f:
                    f.write(part.get_payload(decode=True))

username = "user_name@gmail.com"
password = "password"

download_email_attachments(username, password)

print('done!')
