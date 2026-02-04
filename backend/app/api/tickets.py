from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import ticket as models
from app.schemas import ticket as schemas
from app.tasks.ticket_processing import process_ticket

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tickets/", response_model=schemas.TicketResponse)
def create_ticket(
    ticket: schemas.TicketCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_ticket = models.Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # Trigger background AI processing
    background_tasks.add_task(process_ticket, db_ticket.id)
    
    return db_ticket

@router.get("/tickets/", response_model=List[schemas.TicketResponse])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).offset(skip).limit(limit).all()
    return tickets

@router.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
