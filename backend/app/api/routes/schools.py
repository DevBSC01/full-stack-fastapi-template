import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import School, SchoolCreate, SchoolUpdate, SchoolPublic, Message

router = APIRouter(prefix="/schools", tags=["schools"])


@router.get("/", response_model=list[SchoolPublic])
def read_schools(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve schools.
    """
    statement = select(School).offset(skip).limit(limit)
    schools = session.exec(statement).all()
    return schools


@router.get("/{id}", response_model=SchoolPublic)
def read_school(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get school by ID.
    """
    school = session.get(School, id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.post("/", response_model=SchoolPublic)
def create_school(
    *, session: SessionDep, current_user: CurrentUser, school_in: SchoolCreate
) -> Any:
    """
    Create new school.
    """
    school = School.model_validate(school_in)
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


@router.put("/{id}", response_model=SchoolPublic)
def update_school(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    school_in: SchoolUpdate,
) -> Any:
    """
    Update a school.
    """
    school = session.get(School, id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    update_dict = school_in.model_dump(exclude_unset=True)
    school.sqlmodel_update(update_dict)
    session.add(school)
    session.commit()
    session.refresh(school)
    return school


@router.delete("/{id}")
def delete_school(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a school.
    """
    school = session.get(School, id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    session.delete(school)
    session.commit()
    return Message(message="School deleted successfully")
