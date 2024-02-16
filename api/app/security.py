from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from passlib.hash import pbkdf2_sha256

from config import Configuration


SECRET_KEY = Configuration.get("SECURITY", "SECRET_KEY")
ALGORITHM = Configuration.get("SECURITY", "ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = Configuration.get("SECURITY",
                                                "ACCESS_TOKEN_EXPIRE_MINUTES")

SERVICE_TOKEN = Configuration.get("SECURITY", "SERVICE_TOKEN")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
sec = HTTPBasic()


def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pbkdf2_sha256.hash(password)