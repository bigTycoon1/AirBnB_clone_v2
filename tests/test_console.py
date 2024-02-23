#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from models import storage_type

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models

    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for k in kwargs:
                if k in ['created_at', 'updated_at']:
                    setattr(self, k, datetime.fromisoformat(kwargs[k]))
                elif k != '__class__':
                    setattr(self, k, kwargs[k])
            if storage_type == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Return a str representation of the BaseModel"""
        return '[{}] ({}) {}'.format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convertion of BaseModel into dict format"""
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        for k in my_dict:
            if type(my_dct[k]) is datetime:
                my_dict[k] = my_dict[k].isoformat()
        if '_sa_instance_state' in my_dict.keys():
            del(my_dict['_sa_instance_state'])
        return my_dict

    def delete(self):
        '''deletes the current BaseModel from the storage'''
        from models import storage
        storage.delete(self)