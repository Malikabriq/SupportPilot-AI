import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.database import SessionLocal, engine, Base
from app.models.ticket import Ticket
from app.api.tickets import create_ticket

# Create tables
Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    # Check if data exists
    if db.query(Ticket).count() == 0:
        tickets = [
            Ticket(subject="Login Issue", description="Whatever I do i cannot login.", sender_email="john@example.com", status="Open", priority="High", category="Bug"),
            Ticket(subject="Feature Request", description="Dark mode please", sender_email="jane@example.com", status="New", priority="Medium", category="Feature")
        ]
        db.add_all(tickets)
        db.commit()
        print("Data seeded.")
    else:
        print("Data already exists.")
    db.close()

if __name__ == "__main__":
    seed()
