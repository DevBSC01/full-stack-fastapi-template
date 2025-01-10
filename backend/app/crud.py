import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate
from app.models import CV, Job, Task, Skill, School, Contact, Knowledge, Language, Certificate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# CRUD operations for CV
def create_cv(*, session: Session, cv_data: dict) -> CV:
    db_cv = CV(**cv_data)
    session.add(db_cv)
    session.commit()
    session.refresh(db_cv)
    return db_cv

def get_cv(*, session: Session, cv_id: uuid.UUID) -> CV | None:
    return session.get(CV, cv_id)

def update_cv(*, session: Session, cv_id: uuid.UUID, cv_data: dict) -> CV:
    db_cv = session.get(CV, cv_id)
    if db_cv:
        for key, value in cv_data.items():
            setattr(db_cv, key, value)
        session.add(db_cv)
        session.commit()
        session.refresh(db_cv)
    return db_cv

def delete_cv(*, session: Session, cv_id: uuid.UUID) -> None:
    db_cv = session.get(CV, cv_id)
    if db_cv:
        session.delete(db_cv)
        session.commit()

# CRUD operations for Job
def create_job(*, session: Session, job_data: dict) -> Job:
    db_job = Job(**job_data)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job

def get_job(*, session: Session, job_id: uuid.UUID) -> Job | None:
    return session.get(Job, job_id)

def update_job(*, session: Session, job_id: uuid.UUID, job_data: dict) -> Job:
    db_job = session.get(Job, job_id)
    if db_job:
        for key, value in job_data.items():
            setattr(db_job, key, value)
        session.add(db_job)
        session.commit()
        session.refresh(db_job)
    return db_job

def delete_job(*, session: Session, job_id: uuid.UUID) -> None:
    db_job = session.get(Job, job_id)
    if db_job:
        session.delete(db_job)
        session.commit()

# CRUD operations for Task
def create_task(*, session: Session, task_data: dict) -> Task:
    db_task = Task(**task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task(*, session: Session, task_id: uuid.UUID) -> Task | None:
    return session.get(Task, task_id)

def update_task(*, session: Session, task_id: uuid.UUID, task_data: dict) -> Task:
    db_task = session.get(Task, task_id)
    if db_task:
        for key, value in task_data.items():
            setattr(db_task, key, value)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task

def delete_task(*, session: Session, task_id: uuid.UUID) -> None:
    db_task = session.get(Task, task_id)
    if db_task:
        session.delete(db_task)
        session.commit()

# CRUD operations for Skill
def create_skill(*, session: Session, skill_data: dict) -> Skill:
    db_skill = Skill(**skill_data)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill

def get_skill(*, session: Session, skill_id: uuid.UUID) -> Skill | None:
    return session.get(Skill, skill_id)

def update_skill(*, session: Session, skill_id: uuid.UUID, skill_data: dict) -> Skill:
    db_skill = session.get(Skill, skill_id)
    if db_skill:
        for key, value in skill_data.items():
            setattr(db_skill, key, value)
        session.add(db_skill)
        session.commit()
        session.refresh(db_skill)
    return db_skill

def delete_skill(*, session: Session, skill_id: uuid.UUID) -> None:
    db_skill = session.get(Skill, skill_id)
    if db_skill:
        session.delete(db_skill)
        session.commit()

# CRUD operations for School
def create_school(*, session: Session, school_data: dict) -> School:
    db_school = School(**school_data)
    session.add(db_school)
    session.commit()
    session.refresh(db_school)
    return db_school

def get_school(*, session: Session, school_id: uuid.UUID) -> School | None:
    return session.get(School, school_id)

def update_school(*, session: Session, school_id: uuid.UUID, school_data: dict) -> School:
    db_school = session.get(School, school_id)
    if db_school:
        for key, value in school_data.items():
            setattr(db_school, key, value)
        session.add(db_school)
        session.commit()
        session.refresh(db_school)
    return db_school

def delete_school(*, session: Session, school_id: uuid.UUID) -> None:
    db_school = session.get(School, school_id)
    if db_school:
        session.delete(db_school)
        session.commit()

# CRUD operations for Contact
def create_contact(*, session: Session, contact_data: dict) -> Contact:
    db_contact = Contact(**contact_data)
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact

def get_contact(*, session: Session, contact_id: uuid.UUID) -> Contact | None:
    return session.get(Contact, contact_id)

def update_contact(*, session: Session, contact_id: uuid.UUID, contact_data: dict) -> Contact:
    db_contact = session.get(Contact, contact_id)
    if db_contact:
        for key, value in contact_data.items():
            setattr(db_contact, key, value)
        session.add(db_contact)
        session.commit()
        session.refresh(db_contact)
    return db_contact

def delete_contact(*, session: Session, contact_id: uuid.UUID) -> None:
    db_contact = session.get(Contact, contact_id)
    if db_contact:
        session.delete(db_contact)
        session.commit()

# CRUD operations for Knowledge
def create_knowledge(*, session: Session, knowledge_data: dict) -> Knowledge:
    db_knowledge = Knowledge(**knowledge_data)
    session.add(db_knowledge)
    session.commit()
    session.refresh(db_knowledge)
    return db_knowledge

def get_knowledge(*, session: Session, knowledge_id: uuid.UUID) -> Knowledge | None:
    return session.get(Knowledge, knowledge_id)

def update_knowledge(*, session: Session, knowledge_id: uuid.UUID, knowledge_data: dict) -> Knowledge:
    db_knowledge = session.get(Knowledge, knowledge_id)
    if db_knowledge:
        for key, value in knowledge_data.items():
            setattr(db_knowledge, key, value)
        session.add(db_knowledge)
        session.commit()
        session.refresh(db_knowledge)
    return db_knowledge

def delete_knowledge(*, session: Session, knowledge_id: uuid.UUID) -> None:
    db_knowledge = session.get(Knowledge, knowledge_id)
    if db_knowledge:
        session.delete(db_knowledge)
        session.commit()

# CRUD operations for Language
def create_language(*, session: Session, language_data: dict) -> Language:
    db_language = Language(**language_data)
    session.add(db_language)
    session.commit()
    session.refresh(db_language)
    return db_language

def get_language(*, session: Session, language_id: uuid.UUID) -> Language | None:
    return session.get(Language, language_id)

def update_language(*, session: Session, language_id: uuid.UUID, language_data: dict) -> Language:
    db_language = session.get(Language, language_id)
    if db_language:
        for key, value in language_data.items():
            setattr(db_language, key, value)
        session.add(db_language)
        session.commit()
        session.refresh(db_language)
    return db_language

def delete_language(*, session: Session, language_id: uuid.UUID) -> None:
    db_language = session.get(Language, language_id)
    if db_language:
        session.delete(db_language)
        session.commit()

# CRUD operations for Certificate
def create_certificate(*, session: Session, certificate_data: dict) -> Certificate:
    db_certificate = Certificate(**certificate_data)
    session.add(db_certificate)
    session.commit()
    session.refresh(db_certificate)
    return db_certificate

def get_certificate(*, session: Session, certificate_id: uuid.UUID) -> Certificate | None:
    return session.get(Certificate, certificate_id)

def update_certificate(*, session: Session, certificate_id: uuid.UUID, certificate_data: dict) -> Certificate:
    db_certificate = session.get(Certificate, certificate_id)
    if db_certificate:
        for key, value in certificate_data.items():
            setattr(db_certificate, key, value)
        session.add(db_certificate)
        session.commit()
        session.refresh(db_certificate)
    return db_certificate

def delete_certificate(*, session: Session, certificate_id: uuid.UUID) -> None:
    db_certificate = session.get(Certificate, certificate_id)
    if db_certificate:
        session.delete(db_certificate)
        session.commit()
