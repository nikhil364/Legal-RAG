from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)

from datetime import datetime


Base = declarative_base()



class Document(Base):

    __tablename__="documents"


    id = Column(
        Integer,
        primary_key=True
    )


    filepath = Column(
        String,
        unique=True
    )


    filename = Column(
        String
    )


    sha256 = Column(
        String
    )


    folder_path = Column(
        String
    )


    indexed = Column(
        Boolean,
        default=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )