"""Object relational mappings."""

from __future__ import annotations
from datetime import datetime
from typing import Optional, Union

from peewee import DateTimeField, ForeignKeyField

from comcatlib import User
from peeweeplus import EnumField
from peeweeplus import HTMLCharField
from peeweeplus import HTMLTextField
from peeweeplus import JSONModel
from peeweeplus import MySQLDatabase
from tenant2tenant import Visibility

from tenantforum.config import CONFIG


__all__ = ['Topic', 'Response']


DATABASE = MySQLDatabase.from_config(CONFIG)
JSON_FIELDS_TOPIC_PATCH = {'title', 'text'}
JSON_FIELDS_TOPIC_POST = {*JSON_FIELDS_TOPIC_PATCH, 'visibility'}
JSON_FIELDS_RESPONSE = {'text'}


class TenantforumModel(JSONModel):  # pylint: disable=R0903
    """Base model for this database."""

    class Meta:     # pylint: disable=R0903,C0115
        database = DATABASE
        schema = database.database


class Topic(TenantforumModel):
    """A topic."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    title = HTMLCharField()
    text = HTMLTextField()
    visibility = EnumField(Visibility, default=Visibility.TENEMENT)
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)

    @classmethod
    def from_json(cls, json: dict, *, user: Optional[Union[User, int]] = None,
                  **kwargs) -> Topic:
        """Creates a topic from a JSON-ish dict."""
        topic = super().from_json(json, only=JSON_FIELDS_TOPIC_POST, **kwargs)
        topic.user = user
        return topic

    def patch_json(self, json: dict, **kwargs) -> Topic:
        """Patches the record using a JSON-ish dict."""
        super().patch_json(json, only=JSON_FIELDS_TOPIC_PATCH, **kwargs)
        self.edited = datetime.now()
        return self


class Response(TenantforumModel):
    """A response to a topic."""

    user = ForeignKeyField(User, column_name='user', on_delete='CASCADE')
    topic = ForeignKeyField(
        Topic, column_name='topic', backref='responses', on_delete='CASCADE')
    text = HTMLTextField(null=True)
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)

    @classmethod
    def from_json(cls, json: dict, *, user: Optional[Union[User, int]] = None,
                  topic: Optional[Union[Topic, int]] = None,
                  **kwargs) -> Response:
        """Creates a response from a JSON-ish dict."""
        response = super().from_json(json, only=JSON_FIELDS_RESPONSE, **kwargs)
        response.user = user
        response.topic = topic
        return response

    def patch_json(self, json: dict, **kwargs) -> Response:
        """Patches the record using a JSON-ish dict."""
        super().patch_json(json, only=JSON_FIELDS_RESPONSE, **kwargs)
        self.edited = datetime.now()
        return self
