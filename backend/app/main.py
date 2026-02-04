from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import tickets

# Create DB tables (simplest migration strategy for now)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SupportPilot AI")

# CORS (Allow Frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "SupportPilot AI Backend Running"}
