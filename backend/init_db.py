from db import engine, SessionLocal
from models import Base, User
from sqlalchemy import text

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users == 0:
            # Create sample users
            user1 = User(
                username="john_doe",
                email="john@example.com",
                password="hashed_password_123",  # In real app, this would be properly hashed
                phone_number="+1234567890",
                balance=100.00
            )
            
            user2 = User(
                username="jane_doe",
                email="jane@example.com",
                password="hashed_password_456",
                phone_number="+0987654321",
                balance=50.00
            )
            
            db.add(user1)
            db.add(user2)
            db.commit()
            
            print("Sample users created successfully!")
            print(f"User 1: {user1.username} (ID: {user1.id})")
            print(f"User 2: {user2.username} (ID: {user2.id})")
        else:
            print(f"Database already has {existing_users} users")
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()