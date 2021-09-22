"""Object relational mappings."""

from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from comcatlib import User
from peeweeplus import JSONModel, MySQLDatabase

from tenantforum.config import CONFIG


__all__ = ['Topic', 'Response']


DATABASE = MySQLDatabase.from_config(CONFIG)


class TenantforumModel(JSONModel):
    """Base model for this database."""

    class Meta:     # pylint: disable=R0903,C0115
        database = DATABASE
        schema = database.database


class Topic(JSONModel):
    """A topic."""

    user = ForeignKeyField(User, column_name='user')
    title = CharField()
    text = TextField()
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)


class Response(JSONModel):
    """A response to a topic."""

    user = ForeignKeyField(User, column_name='user')
    topic = ForeignKeyField(
        Topic, column_name='topic', backref='responses', on_delete='CASCADE')
    text = TextField()
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)
