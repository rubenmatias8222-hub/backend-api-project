from database import SessionLocal, User
from security import hash_password

db = SessionLocal()

user = User(
    username="admin",
    password=hash_password("1234")
)

db.add(user)
db.commit()

print("User added with hashed password 🚀")