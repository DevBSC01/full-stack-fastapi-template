import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Certificate, CertificateCreate, CertificateUpdate, CertificatePublic, Message

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/", response_model=list[CertificatePublic])
def read_certificates(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve certificates.
    """
    statement = select(Certificate).offset(skip).limit(limit)
    certificates = session.exec(statement).all()
    return certificates


@router.get("/{id}", response_model=CertificatePublic)
def read_certificate(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get certificate by ID.
    """
    certificate = session.get(Certificate, id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate


@router.post("/", response_model=CertificatePublic)
def create_certificate(
    *, session: SessionDep, current_user: CurrentUser, certificate_in: CertificateCreate
) -> Any:
    """
    Create new certificate.
    """
    certificate = Certificate.model_validate(certificate_in)
    session.add(certificate)
    session.commit()
    session.refresh(certificate)
    return certificate


@router.put("/{id}", response_model=CertificatePublic)
def update_certificate(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    certificate_in: CertificateUpdate,
) -> Any:
    """
    Update a certificate.
    """
    certificate = session.get(Certificate, id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    update_dict = certificate_in.model_dump(exclude_unset=True)
    certificate.sqlmodel_update(update_dict)
    session.add(certificate)
    session.commit()
    session.refresh(certificate)
    return certificate


@router.delete("/{id}")
def delete_certificate(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a certificate.
    """
    certificate = session.get(Certificate, id)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    session.delete(certificate)
    session.commit()
    return Message(message="Certificate deleted successfully")
