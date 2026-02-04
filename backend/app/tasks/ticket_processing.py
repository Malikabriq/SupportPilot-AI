from app.database import SessionLocal
from app.models.ticket import Ticket
from app.services.ai_classifier import classify_ticket
from app.services.ai_reply_generator import generate_reply

def process_ticket(ticket_id: int):
    """
    Orchestrates the AI processing pipeline for a ticket.
    """
    db = SessionLocal()
    try:
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return
        
        print(f"Processing ticket #{ticket.id}: {ticket.subject}")
        
        # 1. Classify
        classification = classify_ticket(ticket.subject, ticket.description)
        ticket.priority = classification["priority"]
        ticket.category = classification["category"]
        
        # 2. Generate Reply
        reply = generate_reply(ticket.subject, ticket.description, ticket.category)
        ticket.ai_reply = reply
        
        # 3. Update Status
        ticket.status = "In Progress"
        
        db.commit()
        db.refresh(ticket)
        print(f"Ticket #{ticket.id} processed. Priority: {ticket.priority}, Category: {ticket.category}")
    finally:
        db.close()
