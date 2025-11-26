from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from typing import Literal


# --- Profiles --- #
class Profile(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProfileCreate(BaseModel):
    email: str
    full_name: str
    role: str
    password: str  # plain text password


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(Profile):
    pass


class RoleUpdate(BaseModel):
    role: Literal["admin", "team_leader", "operator"]


# --- Departments --- #
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    # frontend’den istersen current user id gönderebilirsin
    created_by: Optional[int] = None
    

class Department(DepartmentBase):
    id: int
    created_at: datetime
    created_by: Optional[int] = None

    class Config:
        orm_mode = True


# --- Machines --- #
class MachineBase(BaseModel):
    machine_code: str
    machine_name: str
    description: Optional[str] = None
    department_id: Optional[int] = None


class Machine(MachineBase):
    id: int
    current_status: str
    last_updated_at: Optional[datetime]
    last_updated_by: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True


# --- Status Types --- #
class StatusType(BaseModel):
    id: int
    name: str
    color: str
    is_default: bool
    is_active: bool
    display_order: int
    created_at: datetime
    created_by: Optional[int] = None

    class Config:
        orm_mode = True


class StatusTypeCreate(BaseModel):
    name: str
    color: str = "gray"
    is_default: bool = False
    is_active: bool = True
    display_order: int = 0
    created_by: Optional[int] = None


class StatusTypeUpdate(BaseModel):
    name: str
    color: str


# --- Status History --- #
class StatusHistory(BaseModel):
    id: int
    machine_id: int
    status: str
    previous_status: Optional[str] = None
    comment: Optional[str] = None
    changed_by: int
    changed_at: datetime

    class Config:
        orm_mode = True


class StatusUpdateRequest(BaseModel):
    status: str
    comment: str | None = None
    changed_by: int


# --- Department Leaders --- #
class DepartmentLeaderBase(BaseModel):
    department_id: int
    user_id: int
    assigned_by: Optional[int] = None


class DepartmentLeader(DepartmentLeaderBase):
    id: int
    assigned_at: datetime

    class Config:
        orm_mode = True


# --- Machine Operators --- #
class MachineOperatorBase(BaseModel):
    machine_id: int
    user_id: int
    assigned_by: Optional[int] = None


class MachineOperator(MachineOperatorBase):
    id: int
    assigned_at: datetime

    class Config:
        orm_mode = True