from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine('sqlite:///./test.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Session | None:
    try:
        session = SessionLocal()
        return session
    except:
        return None
    
from sqlalchemy import create_engine, text
        
if __name__ == "__main__":
    db = get_db()
    if db:
        print("Connected Successfully")
    else:
        print("Not connected")