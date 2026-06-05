from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, Student, Notification, NotificationStudent
from datetime import datetime, timedelta
import requests
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from logging_middleware.config import *
from logging_middleware.log import get_access_token
from logging_utils import safe_log

import random


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

safe_log("database module loaded")


def get_db() -> Session | None:
    safe_log("creating database session")
    try:
        session = SessionLocal()
        safe_log("database session created")
        return session
    except Exception:
        safe_log("failed to create database session", level="error")
        return None


def init_db(seed: bool = False) -> None:
    safe_log(f"initializing database seed={seed}")
    Base.metadata.create_all(bind=engine)
    safe_log("database tables ensured")
    if seed:
        safe_log("starting seed process")
        db = get_db()
        if not db:
            safe_log("seed aborted because database session was unavailable", level="error")
            return
        if not db.query(Student).first():
            safe_log("seeding default students")
            alice = Student(id=1, name="Alice")
            bob = Student(id=2, name="Bob")
            db.add_all([alice, bob])
            db.commit()
            safe_log("default students seeded")

        if not db.query(Notification).first():
            safe_log("fetching notification seed payload from API")
            response = requests.get(BASE_URL + "/notifications", 
                headers= {
                    "Authorization": ' '.join(get_access_token())
                }
            ).json()['notifications']
            safe_log(f"received {len(response)} notifications from API")
            
            for res in response:
                n = Notification(
                    type=res["Type"],
                    message=res["Message"],
                )
            
                db.add(n)
            db.commit()
            safe_log("notification seed rows committed")
            
            for i in range(1, 3):
                for _ in range(5):
                    id = random.choice(response)["ID"]
                    ns = NotificationStudent(student_id=1, notification_id=id, is_viewed=True)
                    db.add(ns)
            db.commit()
            safe_log("notification-student seed rows committed")
        db.close()
        safe_log("database session closed after seeding")


if __name__ == "__main__":
    safe_log("running database seeding from module entrypoint")
    init_db(seed=True)
    print("DB initialized (seeded)")