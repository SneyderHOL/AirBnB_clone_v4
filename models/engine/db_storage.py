#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None
    classes = {"Amenity": Amenity, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        ''' Query all objects in current db '''
        r_dic = {}
        if cls is not None:
            query = self.__session.query(cls)
            for res in query:
                k = res.__class__.__name__ + '.' + res.id
                r_dic[k] = res
        else:
            for k, v in DBStorage.classes.items():
                # if not isinstance(v, type(BaseModel)):
                query = self.__session.query(v).all()
                for res in query:
                    k = res.__class__.__name__ + '.' + res.id
                    r_dic[k] = res
        return r_dic

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """method that retrive an object """
        all_els = self.all(cls)
        key = cls.__name__ + '.' + id
        if key in all_els:
            return (all_els[key])
        else:
            return (None)

    def count(self, cls=None):
        """ method that count the number of objects in storage: """
        all_els = self.all(cls)
        return (len(all_els))
