from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    subject: str
    description: str
    sender_email: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    ai_reply: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    status: str
    priority: Optional[str] = None
    category: Optional[str] = None
    ai_reply: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
