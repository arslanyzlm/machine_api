from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .database import Base


def now_utc():
    return datetime.now(timezone.utc)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, nullable=False, unique=True)
    full_name = Column(Text, nullable=False)
    role = Column(Text, nullable=False)  # admin / team_leader / operator
    password_hash = Column(Text, nullable=False)  # YENİ
    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)

    # İstersen ilişki alanları:
    # departments_created = relationship("Department", back_populates="created_by_user")
    # machines_updated = relationship("Machine", back_populates="last_updated_user")
    # vs. ekleyebilirsin, ama şart değil.

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    created_by = Column(Integer, ForeignKey("profiles.id"), nullable=True)

    machines = relationship("Machine", back_populates="department")
    # created_by_user = relationship("Profile", back_populates="departments_created")


class DepartmentLeader(Base):
    __tablename__ = "department_leaders"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    assigned_by = Column(Integer, ForeignKey("profiles.id"), nullable=True)

    # department = relationship("Department")
    # user = relationship("Profile", foreign_keys=[user_id])


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_code = Column(Text, nullable=False)
    machine_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    current_status = Column(Text, nullable=False, default="")
    last_updated_at = Column(DateTime(timezone=True), nullable=True)
    last_updated_by = Column(Integer, ForeignKey("profiles.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", back_populates="machines")

    status_history = relationship("StatusHistory", back_populates="machine")


class MachineOperator(Base):
    __tablename__ = "machine_operators"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    assigned_by = Column(Integer, ForeignKey("profiles.id"), nullable=True)

    # machine = relationship("Machine")
    # user = relationship("Profile", foreign_keys=[user_id])


class StatusType(Base):
    __tablename__ = "status_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True)
    color = Column(Text, nullable=False, default="gray")
    is_default = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    created_by = Column(Integer, ForeignKey("profiles.id"), nullable=True)


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    status = Column(Text, nullable=False)
    previous_status = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    changed_by = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    changed_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)

    machine = relationship("Machine", back_populates="status_history")
    # changed_by_user = relationship("Profile", foreign_keys=[changed_by])

