#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os

class DBStorage:
    """This class manages storage of models in a MySQL database using SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Create an engine linked to MySQL database and user."""
        user = os.getenv('DD_MYSQL_USER')
        password = os.getenv('Great#7729')
        host = os.getenv('DD_MYSQL_HOST', 'localhost')
        database = os.getenv('DD_MYSQL_DB')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True
        )

        if os.getenv('DD_ENV') == 'test':
            self.__drop_all()

        self.__session = None

    def all(self, cls=None):
        """Return a dictionary of all objects."""
        if cls:
            if isinstance(cls, str):
                cls = self.classes[cls]
            objs = self.__session.query(cls).all()
        else:
            objs = self.__session.query(Base).all()

        all_objs = {}
        for obj in objs:
            cls_name = obj.__class__.__name__
            all_objs[f"{cls_name}.{obj.id}"] = obj
        return all_objs

    def new(self, obj):
        """Add a new object to the current session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and create a new session."""
        from models import state, city, amenity, place, review  # Import all models here
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def __drop_all(self):
        """Drop all tables in the database."""
        Base.metadata.drop_all(self.__engine)
