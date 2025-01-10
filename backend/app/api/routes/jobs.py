import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Job, JobCreate, JobUpdate, JobPublic, Message

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=list[JobPublic])
def read_jobs(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve jobs.
    """
    statement = select(Job).offset(skip).limit(limit)
    jobs = session.exec(statement).all()
    return jobs


@router.get("/{id}", response_model=JobPublic)
def read_job(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get job by ID.
    """
    job = session.get(Job, id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=JobPublic)
def create_job(
    *, session: SessionDep, current_user: CurrentUser, job_in: JobCreate
) -> Any:
    """
    Create new job.
    """
    job = Job.model_validate(job_in)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@router.put("/{id}", response_model=JobPublic)
def update_job(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    job_in: JobUpdate,
) -> Any:
    """
    Update a job.
    """
    job = session.get(Job, id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    update_dict = job_in.model_dump(exclude_unset=True)
    job.sqlmodel_update(update_dict)
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


@router.delete("/{id}")
def delete_job(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a job.
    """
    job = session.get(Job, id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return Message(message="Job deleted successfully")
