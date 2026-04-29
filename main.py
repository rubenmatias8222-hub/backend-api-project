from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, User
from security import verify_password
from auth import create_access_token

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# REQUEST MODEL
class LoginRequest(BaseModel):
    username: str
    password: str

# ROOT
@app.get("/")
def read_root():
    return {"message": "FastAPI is working 🚀"}

# LOGIN
@app.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_user and verify_password(user.password, db_user.password):
        token = create_access_token({"sub": user.username})

        return {
            "message": "Login successful 🚀",
            "access_token": token,
            "token_type": "bearer"
        }

    return {"message": "Invalid credentials ❌"}