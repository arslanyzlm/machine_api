from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/department-leaders", tags=["department_leaders"])


@router.get("/", response_model=List[schemas.DepartmentLeader])
def list_department_leaders(
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
):
    q = db.query(models.DepartmentLeader)
    if user_id is not None:
        q = q.filter(models.DepartmentLeader.user_id == user_id)
    return q.all()


@router.post("/", response_model=schemas.DepartmentLeader)
def create_department_leader(
    payload: schemas.DepartmentLeaderBase,
    db: Session = Depends(get_db),
):
    leader = models.DepartmentLeader(
        department_id=payload.department_id,
        user_id=payload.user_id,
        assigned_by=payload.assigned_by,
    )
    db.add(leader)
    db.commit()
    db.refresh(leader)
    return leader


@router.delete("/{leader_id}")
def delete_department_leader(
    leader_id: int,
    db: Session = Depends(get_db),
):
    row = db.query(models.DepartmentLeader).filter(models.DepartmentLeader.id == leader_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Department leader not found")

    db.delete(row)
    db.commit()
    return {"success": True}