import imaplib
import email
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = "emilykelt.blogs@gmail.com"
EMAIL_PASS = "gebmoz-rocnez-6Ryxwo"

def fetch_emails():
    # Connect to the server and log in
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)

    # Select the mailbox
    mail.select("inbox")

    # Search for unread emails
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    posts = []
    for email_id in email_ids:
        # Fetch the email
        res, msg = mail.fetch(email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # Parse the email
                msg = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            posts.append({"title": subject, "content": body})
                else:
                    body = msg.get_payload(decode=True).decode()
                    posts.append({"title": subject, "content": body})

    # Close the connection
    mail.logout()
    return posts
