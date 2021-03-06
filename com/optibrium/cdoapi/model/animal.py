from com.optibrium.cdoapi.model import database
from sqlalchemy import Column, ForeignKey, Integer, String


class Animal(database.Model):

    __tablename__ = 'animals'

    id = Column('id', Integer, primary_key=True)

    name = Column('name', String, unique=True)

    species = Column('species', String)

    owner = Column('owner', Integer, ForeignKey('owners.id'))
