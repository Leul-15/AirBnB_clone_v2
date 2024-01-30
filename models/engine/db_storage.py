#!/usr/bin/python3
"""Define class DatabaseStorage
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship
from models.state import State
from models.city import City
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


class DBStorage:
    """Create SQLalchemy database
    """
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and link to MySQL databse"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB"),
                                             pool_pre_ping=True))
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query current database session
        """
        if cls is None:
            new_objs = self.__session.query(State).all()
            new_objs.extend(self.__session.query(City).all())
            new_objs.extend(self.__session.query(User).all())
            new_objs.extend(self.__session.query(Place).all())
            new_objs.extend(self.__session.query(Review).all())
            new_objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            new_objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in new_objs}

    def new(self, obj):
        """Add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Commit all changes of current database session
        """
        Base.metadata.create_all(self.__engine)
        session_fact = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(session_fact)
        self.__session = Session()

    def close(self):
        """Close working SQLalchemy session
        """
        self.__session.close()
