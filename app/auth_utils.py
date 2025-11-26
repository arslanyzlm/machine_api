# app/auth_utils.py
from passlib.context import CryptContext

# Sadece resmi bcrypt backend'i kullanan bir context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    default="bcrypt",
    bcrypt__ident="2b",     # modern bcrypt formatı
    deprecated="auto",
)

MAX_BCRYPT_LENGTH = 72


def _normalize_password(password: str) -> str:
    """
    bcrypt'in 72 byte limitine takılmaması için
    string'i truncate ediyoruz.
    """
    if not isinstance(password, str):
        password = str(password)

    # UTF-8 byte uzunluğu yerine güvenli taraf için karakter bazlı truncation:
    if len(password) > MAX_BCRYPT_LENGTH:
        password = password[:MAX_BCRYPT_LENGTH]
    return password


def get_password_hash(password: str) -> str:
    """
    Şifreyi hashler, bcrypt limitlerini güvenli şekilde uygular.
    """
    print(password)
    password = _normalize_password(password)
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Girilen şifreyi, veri tabanındaki hash ile karşılaştırır.
    """
    password = _normalize_password(password)
    return pwd_context.verify(password, hashed_password)
