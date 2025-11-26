from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..auth_utils import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=schemas.LoginResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Basit login endpoint'i:
    - email + password alır
    - profiles tablosunda kullanıcıyı bulur
    - password_hash ile karşılaştırır
    - doğruysa Profile (LoginResponse) döner
    """
    # 1) Email ile kullanıcıyı bul
    user = (
        db.query(models.Profile)
        .filter(models.Profile.email == payload.email)
        .first()
    )

    if not user:
        # Bilerek generic mesaj veriyoruz
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 2) Şifreyi verify et
    if not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # 3) Başarılı -> ProfileOut döndür
    return user
