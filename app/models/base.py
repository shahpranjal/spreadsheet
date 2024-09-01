from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr
from datetime import date, datetime
import json


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self):
        def serialize(value):
            if isinstance(value, (datetime, date)):
                return value.isoformat()
            return value

        return {c.name: serialize(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __str__(self):
        return self.__repr__()
