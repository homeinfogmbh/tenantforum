"""Common functions."""

from typing import Union

from peewee import Expression, ModelSelect

from comcatlib import User
from mdb import Customer, Tenement
from tenant2tenant import Visibility

from tenantforum.orm import Topic, Response


__all__ = [
    'get_visible_topics',
    'get_own_topic',
    'get_topics',
    'get_visible_responses',
    'get_responses',
    'get_own_response'
]


def get_visibility_condition(user: User) -> Expression:
    """Returns a select expression."""

    return (
        (
            (Topic.visibility == Visibility.CUSTOMER)
            & (Tenement.customer == user.customer)
        )
        | (
            (Topic.visibility == Visibility.TENEMENT)
            & (User.tenement == user.tenement)
        )
    )


def get_visible_topics(user: User) -> ModelSelect:
    """Selects topics visible to the user."""

    return Topic.select().join(User).join(Tenement).where(
        (Topic.user == user) | get_visibility_condition(user)
    )


def get_own_topic(ident: int, user: User) -> Topic:
    """Selects an own topic."""

    return Topic.select().where((Topic.id == ident) & (Topic.user == user))


def get_topics(customer: Customer) -> ModelSelect:
    """Selects topics of a certain customer."""

    return Topic.select().join(User).join(Tenement).where(
        Tenement.customer == customer)


def get_visible_responses(topic: Union[Topic, int], user: User) -> ModelSelect:
    """Selects responses to a topic visible to the given user."""

    condition = (
        (Response.topic == topic)
        & (
            (Response.user == user) | get_visibility_condition(user)
        )
    )
    return Response.select().join(Topic).join(User).join(Tenement).where(
        condition)


def get_responses(topic: Union[Topic, int], customer: Customer) -> ModelSelect:
    """Selects responses to a topic for a given customer."""

    condition = (
        (Response.topic == topic)
        & (Tenement.customer == customer)
    )
    return Response.select().join(Topic).join(User).join(Tenement).where(
        condition)


def get_own_response(ident: int, user: User) -> Response:
    """Selects an own response."""

    condition = (Response.id == ident) & (Response.user == user)
    return Response.select().where(condition)