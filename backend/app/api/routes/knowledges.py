import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Knowledge, KnowledgeCreate, KnowledgeUpdate, KnowledgePublic, Message

router = APIRouter(prefix="/knowledges", tags=["knowledges"])


@router.get("/", response_model=list[KnowledgePublic])
def read_knowledges(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve knowledges.
    """
    statement = select(Knowledge).offset(skip).limit(limit)
    knowledges = session.exec(statement).all()
    return knowledges


@router.get("/{id}", response_model=KnowledgePublic)
def read_knowledge(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get knowledge by ID.
    """
    knowledge = session.get(Knowledge, id)
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return knowledge


@router.post("/", response_model=KnowledgePublic)
def create_knowledge(
    *, session: SessionDep, current_user: CurrentUser, knowledge_in: KnowledgeCreate
) -> Any:
    """
    Create new knowledge.
    """
    knowledge = Knowledge.model_validate(knowledge_in)
    session.add(knowledge)
    session.commit()
    session.refresh(knowledge)
    return knowledge


@router.put("/{id}", response_model=KnowledgePublic)
def update_knowledge(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    knowledge_in: KnowledgeUpdate,
) -> Any:
    """
    Update a knowledge.
    """
    knowledge = session.get(Knowledge, id)
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    update_dict = knowledge_in.model_dump(exclude_unset=True)
    knowledge.sqlmodel_update(update_dict)
    session.add(knowledge)
    session.commit()
    session.refresh(knowledge)
    return knowledge


@router.delete("/{id}")
def delete_knowledge(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a knowledge.
    """
    knowledge = session.get(Knowledge, id)
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    session.delete(knowledge)
    session.commit()
    return Message(message="Knowledge deleted successfully")
