import sys
import os
import imaplib
import email
from email.header import decode_header
import time

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.config import settings
from app.database import SessionLocal
from app.models.ticket import Ticket
from app.tasks.ticket_processing import process_ticket

def fetch_emails():
    print("Connecting to IMAP server...")
    try:
        mail = imaplib.IMAP4_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mail.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        mail.select("inbox")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # Search for unread emails
    status, messages = mail.search(None, 'UNSEEN')
    if status != "OK":
        print("No messages found.")
        return

    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} new emails.")

    db = SessionLocal()
    
    for email_id in email_ids:
        # Fetch the email
        res, msg = mail.fetch(email_id, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                sender = msg.get("From")
                
                # Get body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                print(f"Importing email: {subject}")
                
                # Create Ticket
                new_ticket = Ticket(
                    subject=subject,
                    description=body,
                    sender_email=str(sender),
                    status="Open"
                )
                db.add(new_ticket)
                db.commit()
                db.refresh(new_ticket)
                
                # Trigger Processing
                process_ticket(db, new_ticket.id)
                
    db.close()
    mail.logout()
    print("Email fetch cycle complete.")

if __name__ == "__main__":
    fetch_emails()
