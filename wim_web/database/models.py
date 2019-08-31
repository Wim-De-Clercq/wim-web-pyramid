from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    admin = Column(Boolean, nullable=False, default=False,
                   server_default='false')
    pw_hash = Column(String, nullable=False)


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    files = relationship("File", back_populates="item")
    created_by = relationship("User")


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    extension = Column(String(length=5), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)

    item = relationship("Item", back_populates="files")

