from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/machine-operators", tags=["machine_operators"])


@router.get("/", response_model=List[schemas.MachineOperator])
def list_machine_operators(
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
    machine_id: Optional[int] = None,
):
    q = db.query(models.MachineOperator)
    if user_id is not None:
        q = q.filter(models.MachineOperator.user_id == user_id)
    if machine_id is not None:
        q = q.filter(models.MachineOperator.machine_id == machine_id)
    return q.all()


@router.post("/", response_model=schemas.MachineOperator)
def create_machine_operator(
    payload: schemas.MachineOperatorBase,
    db: Session = Depends(get_db),
):
    op = models.MachineOperator(
        machine_id=payload.machine_id,
        user_id=payload.user_id,
        assigned_by=payload.assigned_by,
    )
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@router.delete("/{op_id}")
def delete_machine_operator(
    op_id: int,
    db: Session = Depends(get_db),
):
    row = db.query(models.MachineOperator).filter(models.MachineOperator.id == op_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Machine operator not found")

    db.delete(row)
    db.commit()
    return {"success": True}
