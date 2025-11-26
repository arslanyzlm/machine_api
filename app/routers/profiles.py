# app/routers/profiles.py
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..auth_utils import get_password_hash

from ..database import get_db
from .. import models, schemas
from ..schemas import RoleUpdate


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/", response_model=List[schemas.Profile])
def list_profiles(
    db: Session = Depends(get_db),
    role: Optional[str] = None,
    ids: Optional[str] = Query(None, description="Comma-separated profile ids"),
):
    q = db.query(models.Profile)

    if role:
        q = q.filter(models.Profile.role == role)

    if ids:
        id_list = [int(x) for x in ids.split(",") if x]
        if id_list:
            q = q.filter(models.Profile.id.in_(id_list))

    return q.order_by(models.Profile.full_name).all()

@router.get("/{profile_id}", response_model=schemas.Profile)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=schemas.Profile)
def create_profile(payload: schemas.ProfileCreate, db: Session = Depends(get_db)):
    # Aynı email var mı kontrolü
    existing = (  
        db.query(models.Profile)
        .filter(models.Profile.email == payload.email)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = models.Profile(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        password_hash=get_password_hash(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user



@router.put("/{profile_id}/role", response_model=schemas.Profile)
def update_role(
    profile_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
):
    profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile.role = payload.role
    db.commit()
    db.refresh(profile)
    return profile