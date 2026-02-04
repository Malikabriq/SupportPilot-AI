from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    description = Column(Text)
    sender_email = Column(String, index=True)
    
    # Status: Open, In Progress, Resolved, Closed
    status = Column(String, default="Open")
    
    # AI Fields
    priority = Column(String, nullable=True) # Low, Medium, High
    category = Column(String, nullable=True) # Bug, Feature, Billing, etc.
    ai_reply = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
