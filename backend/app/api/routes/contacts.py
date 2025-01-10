import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Contact, ContactCreate, ContactUpdate, ContactPublic, Message

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactPublic])
def read_contacts(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve contacts.
    """
    statement = select(Contact).offset(skip).limit(limit)
    contacts = session.exec(statement).all()
    return contacts


@router.get("/{id}", response_model=ContactPublic)
def read_contact(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get contact by ID.
    """
    contact = session.get(Contact, id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactPublic)
def create_contact(
    *, session: SessionDep, current_user: CurrentUser, contact_in: ContactCreate
) -> Any:
    """
    Create new contact.
    """
    contact = Contact.model_validate(contact_in)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


@router.put("/{id}", response_model=ContactPublic)
def update_contact(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    contact_in: ContactUpdate,
) -> Any:
    """
    Update a contact.
    """
    contact = session.get(Contact, id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    update_dict = contact_in.model_dump(exclude_unset=True)
    contact.sqlmodel_update(update_dict)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact


@router.delete("/{id}")
def delete_contact(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a contact.
    """
    contact = session.get(Contact, id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    session.delete(contact)
    session.commit()
    return Message(message="Contact deleted successfully")
