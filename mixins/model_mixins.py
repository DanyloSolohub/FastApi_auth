import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy_mixins import AllFeaturesMixin

from utils.database import Base, Session


class IDPrimaryKeyABC(Base, AllFeaturesMixin):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)

    @property
    def pk(self):
        return self.id

    @pk.setter
    def pk(self, pk):
        self.id = pk


class Name(Base, AllFeaturesMixin):
    __abstract__ = True

    name = sa.Column(sa.String(255))
    name_ukr = sa.Column(sa.String(255))
    name_eng = sa.Column(sa.String(255))


class Date(Base, AllFeaturesMixin):
    __abstract__ = True

    created_at = sa.Column(sa.DateTime, server_default=func.now())
    modified_at = sa.Column(sa.DateTime, onupdate=func.now())


IDPrimaryKeyABC.set_session(Session)
Name.set_session(Session)
Date.set_session(Session)
