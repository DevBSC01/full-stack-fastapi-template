import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class CVBase(SQLModel):
    name: str = Field(max_length=255)
    recipient: str = Field(max_length=255)


class CVCreate(CVBase):
    pass


class CVUpdate(CVBase):
    name: str | None = Field(default=None, max_length=255)
    recipient: str | None = Field(default=None, max_length=255)


class CVPublic(CVBase):
    id: uuid.UUID
    created_at: datetime
    edited_at: datetime


class CVsPublic(SQLModel):
    data: list[CVPublic]
    count: int


class CV(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    edited_at: datetime = Field(default_factory=datetime.utcnow)
    recipient: str = Field(max_length=255)
    jobs: list["Job"] = Relationship(back_populates="cv")
    schools: list["School"] = Relationship(back_populates="cv")
    contact: "Contact" = Relationship(back_populates="cv", sa_relationship_kwargs={"uselist": False})


class JobBase(SQLModel):
    position: str = Field(max_length=255)
    company: str = Field(max_length=255)
    location: str = Field(max_length=255)
    start: datetime
    end: datetime | None = None


class JobCreate(JobBase):
    cv_id: uuid.UUID


class JobUpdate(JobBase):
    position: str | None = Field(default=None, max_length=255)
    company: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    start: datetime | None = None
    end: datetime | None = None


class JobPublic(JobBase):
    id: uuid.UUID
    cv_id: uuid.UUID


class Job(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    position: str = Field(max_length=255)
    company: str = Field(max_length=255)
    location: str = Field(max_length=255)
    start: datetime
    end: datetime | None = None
    cv_id: uuid.UUID = Field(foreign_key="cv.id")
    cv: CV = Relationship(back_populates="jobs")
    tasks: list["Task"] = Relationship(back_populates="job")


class TaskBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    duration: int


class TaskCreate(TaskBase):
    job_id: uuid.UUID


class TaskUpdate(TaskBase):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    duration: int | None = None


class TaskPublic(TaskBase):
    id: uuid.UUID
    job_id: uuid.UUID


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    duration: int
    job_id: uuid.UUID = Field(foreign_key="job.id")
    job: Job = Relationship(back_populates="tasks")
    skills: list["Skill"] = Relationship(back_populates="task")


class SkillBase(SQLModel):
    name: str = Field(max_length=255)
    rating: int


class SkillCreate(SkillBase):
    task_id: uuid.UUID


class SkillUpdate(SkillBase):
    name: str | None = Field(default=None, max_length=255)
    rating: int | None = None


class SkillPublic(SkillBase):
    id: uuid.UUID
    task_id: uuid.UUID


class Skill(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    rating: int
    task_id: uuid.UUID = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="skills")


class KnowledgeBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    rating: int


class KnowledgeCreate(KnowledgeBase):
    pass


class KnowledgeUpdate(KnowledgeBase):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    rating: int | None = None


class KnowledgePublic(KnowledgeBase):
    id: uuid.UUID


class Knowledge(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    rating: int


class SchoolBase(SQLModel):
    school: str = Field(max_length=255)
    subject: str = Field(max_length=255)
    degree: str = Field(max_length=255)
    location: str = Field(max_length=255)
    start: datetime
    end: datetime | None = None


class SchoolCreate(SchoolBase):
    cv_id: uuid.UUID


class SchoolUpdate(SchoolBase):
    school: str | None = Field(default=None, max_length=255)
    subject: str | None = Field(default=None, max_length=255)
    degree: str | None = Field(default=None, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    start: datetime | None = None
    end: datetime | None = None


class SchoolPublic(SchoolBase):
    id: uuid.UUID
    cv_id: uuid.UUID


class School(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    school: str = Field(max_length=255)
    subject: str = Field(max_length=255)
    degree: str = Field(max_length=255)
    location: str = Field(max_length=255)
    start: datetime
    end: datetime | None = None
    cv_id: uuid.UUID = Field(foreign_key="cv.id")
    cv: CV = Relationship(back_populates="schools")


# 
# Contact models
#

class ContactBase(SQLModel):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    address: str = Field(max_length=255)
    zip_code: str = Field(max_length=20)
    location: str = Field(max_length=255)
    phone: str = Field(max_length=20)
    email: EmailStr
    birthdate: datetime
    photo: str | None = Field(default=None, max_length=255)
    marital_status: str | None = Field(default=None, max_length=255)
    
class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=255)
    zip_code: str | None = Field(default=None, max_length=20)
    location: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = Field(default=None)
    birthdate: datetime | None = None
    photo: str | None = Field(default=None, max_length=255)
    marital_status: str | None = Field(default=None, max_length=255)
    
class ContactPublic(ContactBase):
    id: uuid.UUID

class Contact(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    address: str = Field(max_length=255)
    zip_code: str = Field(max_length=20)
    location: str = Field(max_length=255)
    phone: str = Field(max_length=20)
    email: EmailStr
    birthdate: datetime
    photo: str | None = Field(default=None, max_length=255)
    marital_status: str | None = Field(default=None, max_length=255)
    cv_id: uuid.UUID = Field(foreign_key="cv.id")
    cv: CV = Relationship(back_populates="contact")


class LanguageBase(SQLModel):
    language: str = Field(max_length=255)
    level: str = Field(max_length=255)


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    language: str | None = Field(default=None, max_length=255)
    level: str | None = Field(default=None, max_length=255)


class LanguagePublic(LanguageBase):
    id: uuid.UUID


class Language(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    language: str = Field(max_length=255)
    level: str = Field(max_length=255)


#
# C
#


class CertificateBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    date: datetime


class CertificateCreate(CertificateBase):
    pass


class CertificateUpdate(CertificateBase):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    date: datetime | None = None


class CertificatePublic(CertificateBase):
    id: uuid.UUID


class Certificate(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    date: datetime
