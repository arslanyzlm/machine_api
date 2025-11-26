from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/status-types", tags=["status_types"])


@router.get("/", response_model=List[schemas.StatusType])
def list_status_types(
    db: Session = Depends(get_db),
    only_active: bool = True,
):
    q = db.query(models.StatusType)
    if only_active:
        q = q.filter(models.StatusType.is_active == True)
    return q.order_by(models.StatusType.display_order).all()

@router.post("/", response_model=schemas.StatusType)
def create_status_type(
    payload: schemas.StatusTypeCreate,
    db: Session = Depends(get_db),
):
    st = models.StatusType(
        name=payload.name,
        color=payload.color or "gray",
        is_default=payload.is_default,
        is_active=payload.is_active,
        display_order=payload.display_order,
        created_by=payload.created_by,
    )
    db.add(st)
    db.commit()
    db.refresh(st) 
    return st


# update status_type eklenecek 
@router.put("/{status_id}", response_model=schemas.StatusType)
def update_status_type(
    status_id: int,
    payload: schemas.StatusTypeUpdate,
    db: Session = Depends(get_db),
):
    st = db.query(models.StatusType).filter(models.StatusType.id == status_id).first()
    if not st:
        raise HTTPException(status_code=404, detail="Status type not found")

    st.name = payload.name
    st.color = payload.color

    db.commit()
    db.refresh(st)
    return st

