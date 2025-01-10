import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import CV, Job, Task, Skill, School, Contact, Knowledge, Language, Certificate
from app.models import CVCreate, CVUpdate, CVPublic, CVsPublic, Message

router = APIRouter(prefix="/cvs", tags=["cvs"])


@router.get("/", response_model=CVsPublic)
def read_cvs(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve CVs.
    """
    count_statement = select(func.count()).select_from(CV)
    count = session.exec(count_statement).one()
    statement = select(CV).offset(skip).limit(limit)
    cvs = session.exec(statement).all()
    return CVsPublic(data=cvs, count=count)


@router.get("/{id}", response_model=CVPublic)
def read_cv(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get CV by ID.
    """
    cv = session.get(CV, id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    return cv


@router.post("/", response_model=CVPublic)
def create_cv(
    *, session: SessionDep, current_user: CurrentUser, cv_in: CVCreate
) -> Any:
    """
    Create new CV.
    """
    cv = CV.model_validate(cv_in)
    session.add(cv)
    session.commit()
    session.refresh(cv)
    return cv


@router.put("/{id}", response_model=CVPublic)
def update_cv(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    cv_in: CVUpdate,
) -> Any:
    """
    Update a CV.
    """
    cv = session.get(CV, id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    update_dict = cv_in.model_dump(exclude_unset=True)
    cv.sqlmodel_update(update_dict)
    session.add(cv)
    session.commit()
    session.refresh(cv)
    return cv


@router.delete("/{id}")
def delete_cv(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a CV.
    """
    cv = session.get(CV, id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    session.delete(cv)
    session.commit()
    return Message(message="CV deleted successfully")
