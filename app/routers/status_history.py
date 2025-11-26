# app/routers/status_history.py
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/status-history", tags=["status_history"])


@router.get("/", response_model=List[schemas.StatusHistory])
def list_status_history(
    db: Session = Depends(get_db),
    machine_id: Optional[int] = None,
    ascending: bool = False,
):
    q = db.query(models.StatusHistory)
    if machine_id is not None:
        q = q.filter(models.StatusHistory.machine_id == machine_id)

    if ascending:
        q = q.order_by(models.StatusHistory.changed_at.asc())
    else:
        q = q.order_by(models.StatusHistory.changed_at.desc())

    return q.all()
