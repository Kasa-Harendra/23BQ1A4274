from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy import Index, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from logging_utils import safe_log


safe_log("models module loaded")


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    notifications = relationship("NotificationStudent", back_populates="student")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    students = relationship("NotificationStudent", back_populates="notification")


class NotificationStudent(Base):
    __tablename__ = "notification_student_table"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    notification_id: Mapped[str] = mapped_column(ForeignKey("notifications.id"), nullable=False)
    is_viewed: Mapped[bool] = mapped_column(Boolean, default=False)

    student = relationship("Student", back_populates="notifications")
    notification = relationship("Notification", back_populates="students")
    
    __table_args__ = (
        Index("student_id"),
        Index("notification_id")
    )


@event.listens_for(Student, "after_insert")
def log_student_insert(mapper, connection, target):
    safe_log(f"student inserted id={target.id}")


@event.listens_for(Notification, "after_insert")
def log_notification_insert(mapper, connection, target):
    safe_log(f"notification inserted id={target.id} type={target.type}")


@event.listens_for(NotificationStudent, "after_insert")
def log_notification_student_insert(mapper, connection, target):
    safe_log(
        f"notification_student inserted id={target.id} student_id={target.student_id} notification_id={target.notification_id}"
    )


@event.listens_for(NotificationStudent, "after_update")
def log_notification_student_update(mapper, connection, target):
    safe_log(
        f"notification_student updated id={target.id} student_id={target.student_id} notification_id={target.notification_id} viewed={target.is_viewed}"
    )
