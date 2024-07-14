from typing import List
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import relationship
from app.database import Base


class Nodes(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    node = Column(String(100), index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    owner = relationship("Group", back_populates="nodes")


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), index=True)
    city = Column(String(50), index=True)
    nodes = relationship("Nodes", back_populates="owner")


