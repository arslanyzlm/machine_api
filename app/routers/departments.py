from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/", response_model=List[schemas.Department])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).order_by(models.Department.name).all()

@router.post("/", response_model=schemas.Department)
def create_department(
    payload: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
):
    dept = models.Department(
        name=payload.name,
        description=payload.description or "",
        created_by=payload.created_by,
    )
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
    dept = db.query(models.Department).filter(models.Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(dept)
    db.commit()
    return {"success": True}

# Bölüm ekleme işlemi eklenecek
