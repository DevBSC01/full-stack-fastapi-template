import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Language, LanguageCreate, LanguageUpdate, LanguagePublic, Message

router = APIRouter(prefix="/languages", tags=["languages"])


@router.get("/", response_model=list[LanguagePublic])
def read_languages(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve languages.
    """
    statement = select(Language).offset(skip).limit(limit)
    languages = session.exec(statement).all()
    return languages


@router.get("/{id}", response_model=LanguagePublic)
def read_language(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get language by ID.
    """
    language = session.get(Language, id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    return language


@router.post("/", response_model=LanguagePublic)
def create_language(
    *, session: SessionDep, current_user: CurrentUser, language_in: LanguageCreate
) -> Any:
    """
    Create new language.
    """
    language = Language.model_validate(language_in)
    session.add(language)
    session.commit()
    session.refresh(language)
    return language


@router.put("/{id}", response_model=LanguagePublic)
def update_language(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    language_in: LanguageUpdate,
) -> Any:
    """
    Update a language.
    """
    language = session.get(Language, id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    update_dict = language_in.model_dump(exclude_unset=True)
    language.sqlmodel_update(update_dict)
    session.add(language)
    session.commit()
    session.refresh(language)
    return language


@router.delete("/{id}")
def delete_language(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a language.
    """
    language = session.get(Language, id)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    session.delete(language)
    session.commit()
    return Message(message="Language deleted successfully")
