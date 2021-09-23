"""Object relational mappings."""

from __future__ import annotations
from datetime import datetime
from typing import Optional

from peewee import CharField, DateTimeField, ForeignKeyField, TextField

from comcatlib import User
from peeweeplus import JSONModel, MySQLDatabase

from tenantforum.config import CONFIG


__all__ = ['Topic', 'Response']


DATABASE = MySQLDatabase.from_config(CONFIG)
UNCHANGED = object()
ONLY_FIELDS_TOPIC = frozenset({'title', 'text'})
ONLY_FIELDS_RESPONSE = frozenset({'text'})


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

    def edit(self, title: str = UNCHANGED, text: str = UNCHANGED) -> None:
        """Edits the post."""
        self.title = self.title if title is UNCHANGED else title
        self.text = self.text if text is UNCHANGED else text
        self.edited = datetime.now()
        self.save()

    def patch_json(self, json: dict, *, only: set[str] = ONLY_FIELDS_TOPIC,
                   **kwargs) -> Topic:
        """Patches the record using a JSON-ish dict."""
        return super().patch_json(json, only=only, **kwargs)


class Response(TenantforumModel):
    """A response to a topic."""

    user = ForeignKeyField(User, column_name='user')
    topic = ForeignKeyField(
        Topic, column_name='topic', backref='responses', on_delete='CASCADE')
    text = TextField(null=True)
    created = DateTimeField(default=datetime.now)
    edited = DateTimeField(null=True)

    def edit(self, text: Optional[str] = UNCHANGED) -> None:
        """Edits the post."""
        self.text = self.text if text is UNCHANGED else text
        self.edited = datetime.now()
        self.save()

    def blank(self) -> None:
        """Blank this post."""
        self.edit(None)

    def patch_json(self, json: dict, *, only: set[str] = ONLY_FIELDS_RESPONSE,
                   **kwargs) -> Topic:
        """Patches the record using a JSON-ish dict."""
        return super().patch_json(json, only=only, **kwargs)
