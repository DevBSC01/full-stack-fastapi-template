import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Skill, SkillCreate, SkillUpdate, SkillPublic, Message

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/", response_model=list[SkillPublic])
def read_skills(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve skills.
    """
    statement = select(Skill).offset(skip).limit(limit)
    skills = session.exec(statement).all()
    return skills


@router.get("/{id}", response_model=SkillPublic)
def read_skill(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get skill by ID.
    """
    skill = session.get(Skill, id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("/", response_model=SkillPublic)
def create_skill(
    *, session: SessionDep, current_user: CurrentUser, skill_in: SkillCreate
) -> Any:
    """
    Create new skill.
    """
    skill = Skill.model_validate(skill_in)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.put("/{id}", response_model=SkillPublic)
def update_skill(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    skill_in: SkillUpdate,
) -> Any:
    """
    Update a skill.
    """
    skill = session.get(Skill, id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    update_dict = skill_in.model_dump(exclude_unset=True)
    skill.sqlmodel_update(update_dict)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.delete("/{id}")
def delete_skill(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a skill.
    """
    skill = session.get(Skill, id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return Message(message="Skill deleted successfully")
