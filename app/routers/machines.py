# app/routers/machines.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from pydantic import BaseModel
from ..schemas import StatusUpdateRequest

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/machines", tags=["machines"])


@router.get("/", response_model=List[schemas.Machine])
def list_machines(
    db: Session = Depends(get_db),
    department_ids: Optional[str] = Query(
        None, description="Comma-separated department ids"
    ),
    ids: Optional[str] = Query(None, description="Comma-separated machine ids"),
):
    q = db.query(models.Machine)

    if department_ids:
        dept_list = [int(x) for x in department_ids.split(",") if x]
        if dept_list:
            q = q.filter(models.Machine.department_id.in_(dept_list))

    if ids:
        id_list = [int(x) for x in ids.split(",") if x]
        if id_list:
            q = q.filter(models.Machine.id.in_(id_list))

    return q.order_by(models.Machine.machine_code).all()


class MachineCreate(BaseModel):
    machine_code: str
    machine_name: str
    description: str | None = ""
    department_id: int | None = None


@router.post("/", response_model=schemas.Machine)
def create_machine(
    payload: MachineCreate,
    db: Session = Depends(get_db),
):
    machine = models.Machine(
        machine_code=payload.machine_code,
        machine_name=payload.machine_name,
        description=payload.description or "",
        current_status="Beklemede",
        department_id=payload.department_id,
        last_updated_at=datetime.now(timezone.utc),
    )
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine


@router.delete("/{machine_id}")
def delete_machine(
    machine_id: int,
    db: Session = Depends(get_db),
):
    machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    db.delete(machine)
    db.commit()
    return {"success": True}


@router.get("/{machine_id}/history", response_model=List[schemas.StatusHistory])
def machine_history(machine_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.StatusHistory)
        .filter(models.StatusHistory.machine_id == machine_id)
        .order_by(models.StatusHistory.changed_at.asc())
        .all()
    )



@router.post("/{machine_id}/status") #/machines/{machine_id}/status")
def update_machine_status(
    machine_id: int,
    body: StatusUpdateRequest,
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)

    machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    previous_status = machine.current_status

    machine.current_status = body.status
    machine.last_updated_at = now
    machine.last_updated_by = body.changed_by

    history = models.StatusHistory(
        machine_id=machine_id,
        status=body.status,
        previous_status=previous_status,
        comment=body.comment,
        changed_by=body.changed_by,
        changed_at=now,
    )

    db.add(history)
    db.commit()
    db.refresh(machine)
    return machine
