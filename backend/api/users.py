import os
from datetime import datetime

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.middleware import get_current_user
from backend.auth.schemas import UserResponse
from backend.db.models import AlpacaCredential, User
from backend.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])

_fernet = Fernet(os.environ["CREDENTIAL_ENCRYPTION_KEY"].encode())


class CredentialRequest(BaseModel):
    api_key: str
    secret_key: str
    base_url: str


class CredentialStatus(BaseModel):
    has_credentials: bool
    base_url: str | None
    updated_at: datetime | None


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.put("/me/credentials", status_code=status.HTTP_204_NO_CONTENT)
async def upsert_credentials(
    body: CredentialRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    if not body.base_url.startswith("https://"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="base_url must use HTTPS")

    encrypted_api_key = _fernet.encrypt(body.api_key.encode())
    encrypted_secret_key = _fernet.encrypt(body.secret_key.encode())

    credential = await db.scalar(
        select(AlpacaCredential).where(AlpacaCredential.user_id == current_user.id)
    )
    if credential:
        credential.encrypted_api_key = encrypted_api_key
        credential.encrypted_secret_key = encrypted_secret_key
        credential.base_url = body.base_url
    else:
        db.add(AlpacaCredential(
            user_id=current_user.id,
            encrypted_api_key=encrypted_api_key,
            encrypted_secret_key=encrypted_secret_key,
            base_url=body.base_url,
        ))

    await db.commit()


@router.get("/me/credentials", response_model=CredentialStatus)
async def get_credential_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CredentialStatus:
    credential = await db.scalar(
        select(AlpacaCredential).where(AlpacaCredential.user_id == current_user.id)
    )
    return CredentialStatus(
        has_credentials=credential is not None,
        base_url=credential.base_url if credential else None,
        updated_at=credential.updated_at if credential else None,
    )
