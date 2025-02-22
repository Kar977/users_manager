from sqlalchemy import Column, Integer, String, DATE, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, backref, validates

from database_structure.database import sync_engine as db_engine

Base = declarative_base()

VALID_ROLE = (
    "employee",
    "manager",
)

VALID_EMPLOYMENT_STATUS = (
    "full-time",
    "part-time",
    "terminated",
)


class Organization(Base):

    __tablename__ = "organization"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    employees = relationship("Employee", backref("organization"))


class Employee(Base):

    __tablename__ = "employee"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    surname = Column("surname", String)
    birthdate = Column("birthdate", DATE)
    role = Column("role", String, default=VALID_ROLE[0])
    employment_status = Column("employment_status", String)
    organization_id = Column(Integer, ForeignKey("organization.id"))

    @validates("role")
    def validate_role(self, key, role):
        if role not in VALID_ROLE:
            raise ValueError(f"Invalid role: {role}. Must be one of {VALID_ROLE}")
        return role

    @validates("employment_status")
    def validate_employment_status(self, key, employment_status):
        if employment_status not in VALID_EMPLOYMENT_STATUS:
            raise ValueError(
                f"Invalid employment_status {employment_status}. Must be one of {VALID_EMPLOYMENT_STATUS}"
            )
        return employment_status


Base.metadata.create_all(bind=db_engine)
