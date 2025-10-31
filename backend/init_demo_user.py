"""
Initialize demo user for testing
"""
import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, init_db
from app.models.user import User
from app.utils.auth import get_password_hash

async def create_demo_user():
    """Create demo user with email: user@gmail.com, password: 12345678"""
    await init_db()
    
    db: Session = SessionLocal()
    try:
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.email == "user@gmail.com").first()
        
        if existing_user:
            print("✅ Demo user already exists")
            print(f"   Email: user@gmail.com")
            print(f"   Password: 12345678")
            return
        
        # Create demo user
        hashed_password = get_password_hash("12345678")
        demo_user = User(
            email="user@gmail.com",
            username="demo_user",
            hashed_password=hashed_password,
            full_name="Demo User",
            is_active=True
        )
        
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        
        print("✅ Demo user created successfully!")
        print(f"   Email: user@gmail.com")
        print(f"   Password: 12345678")
        print(f"   User ID: {demo_user.id}")
        
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(create_demo_user())

