"""Object relational mappings."""

from __future__ import annotations
from datetime import datetime

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect
from peewee import TextField

from comcatlib import User
from mdb import Company, Customer, Tenement
from peeweeplus import JSONModel, MySQLDatabase

from tenantforum.config import CONFIG


__all__ = ['Topic', 'Response']


DATABASE = MySQLDatabase.from_config(CONFIG)
UNCHANGED = object()


class TenantforumModel(JSONModel):
    """Base model for this database."""

    class Meta:     # pylint: disable=R0903,C0115
        database = DATABASE
        schema = database.database


class Topic(TenantforumModel):
    """A topic."""

    user = ForeignKeyField(User, column_name='user')
    title = CharField()
    text = TextField()
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects records."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, User, Tenement, Customer, Company, *args}
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company)

    def patch_json(self, json: dict, **kwargs) -> Topic:
        """Patches the record using a JSON-ish dict."""
        super().patch_json(json, only={'title', 'text'}, **kwargs)
        self.edited = datetime.now()
        return self


class Response(TenantforumModel):
    """A response to a topic."""

    user = ForeignKeyField(User, column_name='user')
    topic = ForeignKeyField(
        Topic, column_name='topic', backref='responses', on_delete='CASCADE')
    text = TextField(null=True)
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects records."""
        if not cascade:
            return super().select(*args, **kwargs)

        topic_user = User.alias()
        topic_customer = Customer.alias()
        topic_company = Company.alias()
        args = {
            cls, User, Tenement, Customer, Company, Topic, topic_user,
            topic_customer, topic_company, *args
        }
        return super().select(*args, **kwargs).join(User).join(Tenement).join(
            Customer).join(Company).join_from(cls, Topic).join(topic_user).join(
            topic_customer).join(topic_company)

    def patch_json(self, json: dict, **kwargs) -> Topic:
        """Patches the record using a JSON-ish dict."""
        super().patch_json(json, only={'text'}, **kwargs)
        self.edited = datetime.now()
        return self
