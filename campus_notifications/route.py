import time

from fastapi import FastAPI, Depends, Header, HTTPException, status, Request
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import case
from . import db, models
from pydantic import BaseModel
from .logging_utils import safe_log

app = FastAPI()

safe_log("fastapi app created")


class NotificationOut(BaseModel):
    Id: str
    Type: str
    Message: str
    is_viewed: bool


def get_db_session() -> Session:
    session = db.get_db()
    if not session:
        safe_log("failed to acquire database session", level="error")
        raise HTTPException(status_code=500, detail="Could not create DB session")
    try:
        safe_log("yielding database session")
        return session
    finally:
        safe_log("closing database session")
        session.close()


def get_current_student(authorization: str | None = Header(None)) -> int:
    safe_log("parsing authorization header")
    if not authorization:
        safe_log("missing authorization header", level="warning")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        safe_log("invalid authorization header format", level="warning")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = parts[1]
    try:
        student_id = int(token)
        safe_log(f"resolved current student id={student_id}")
    except Exception:
        safe_log("invalid token format", level="warning")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")
    return student_id


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    started_at = time.perf_counter()
    safe_log(f"request started method={request.method} path={request.url.path}")
    try:
        response = await call_next(request)
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        safe_log(
            f"request completed method={request.method} path={request.url.path} status={response.status_code} duration_ms={elapsed_ms}"
        )
        return response
    except Exception as exc:
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        safe_log(
            f"request failed method={request.method} path={request.url.path} duration_ms={elapsed_ms} error={exc}",
            level="error",
        )
        raise


@app.on_event("startup")
def startup_event():
    safe_log("application startup initiated")
    db.init_db(seed=True)
    safe_log("application startup completed")


@app.get("/api/v1/notifications", response_model=List[NotificationOut])
def get_notifications(limit: int = 20, priority: bool = False, current_student: int = Depends(get_current_student), session: Session = Depends(get_db_session)):
    safe_log(f"get_notifications called student_id={current_student} limit={limit} priority={priority}")
    if limit <= 0:
        safe_log("invalid limit requested", level="warning")
        raise HTTPException(status_code=400, detail="limit must be > 0")
    if limit > 50:
        safe_log(f"limit capped from {limit} to 50")
        limit = 50

    if priority:
        safe_log("using priority unread notification ordering")
        max_items = 10
        weight_case = case(
            (models.Notification.type == "Placement", 3),
            (models.Notification.type == "Result", 2),
            (models.Notification.type == "Event", 1),
            else_=0,
        )

        q = (
            session.query(models.Notification, models.NotificationStudent.is_viewed)
            .join(models.NotificationStudent, models.Notification.id == models.NotificationStudent.notification_id)
            .filter(models.NotificationStudent.student_id == current_student)
            .filter(models.NotificationStudent.is_viewed == False)
            .order_by(weight_case.desc(), models.Notification.created_at.desc())
            .limit(max_items)
        )
    else:
        safe_log("using standard notification ordering")
        q = (
            session.query(models.Notification, models.NotificationStudent.is_viewed)
            .join(models.NotificationStudent, models.Notification.id == models.NotificationStudent.notification_id)
            .filter(models.NotificationStudent.student_id == current_student)
            .order_by(models.Notification.created_at.desc())
            .limit(limit)
        )

    results = []
    for notif, is_viewed in q:
        results.append({
            "Id": notif.id,
            "Type": notif.type,
            "Message": notif.message,
            "is_viewed": bool(is_viewed),
        })

    safe_log(f"get_notifications returning count={len(results)}")
    return results


@app.post("/api/v1/notifications/{notification_id}/viewed", response_model=NotificationOut)
def mark_viewed(notification_id: str, current_student: int = Depends(get_current_student), session: Session = Depends(get_db_session)):
    safe_log(f"mark_viewed called student_id={current_student} notification_id={notification_id}")
    assoc = (
        session.query(models.NotificationStudent)
        .filter(models.NotificationStudent.notification_id == notification_id)
        .filter(models.NotificationStudent.student_id == current_student)
        .first()
    )
    if not assoc:
        safe_log("notification not found for student", level="warning")
        raise HTTPException(status_code=404, detail="Notification not found for the student")

    assoc.is_viewed = True
    safe_log("marking notification viewed")
    session.add(assoc)
    session.commit()
    session.refresh(assoc)

    notif = session.query(models.Notification).get(notification_id)
    safe_log("notification marked viewed successfully")
    return {
        "Id": notif.id,
        "Type": notif.type,
        "Message": notif.message,
        "is_viewed": bool(assoc.is_viewed),
    }
