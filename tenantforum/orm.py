"""Object relational mappings."""

from __future__ import annotations
from datetime import datetime

from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from comcatlib import User
from peeweeplus import EnumField, JSONModel, MySQLDatabase
from tenant2tenant import Visibility

from tenantforum.config import CONFIG


__all__ = ['Topic', 'Response']


DATABASE = MySQLDatabase.from_config(CONFIG)
JSON_FIELDS_TOPIC = {'title', 'text'}
JSON_FIELDS_RESPONSE = {'text'}


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
    visibility = EnumField(Visibility, default=Visibility.TENEMENT)
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)

    @classmethod
    def from_json(cls, json: dict, **kwargs) -> Topic:
        """Creates a topic from a JSON-ish dict."""
        return super().from_json(json, only=JSON_FIELDS_TOPIC, **kwargs)

    def patch_json(self, json: dict, **kwargs) -> Topic:
        """Patches the record using a JSON-ish dict."""
        super().patch_json(json, only=JSON_FIELDS_TOPIC, **kwargs)
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
    def from_json(cls, json: dict, **kwargs) -> Response:
        """Creates a response from a JSON-ish dict."""
        return super().from_json(json, only=JSON_FIELDS_RESPONSE, **kwargs)

    def patch_json(self, json: dict, **kwargs) -> Response:
        """Patches the record using a JSON-ish dict."""
        super().patch_json(json, only=JSON_FIELDS_RESPONSE, **kwargs)
        self.edited = datetime.now()
        return self
