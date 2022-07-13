"""Common errors."""

from wsgilib import JSONMessage

from tenantforum.orm import Topic, Response


__all__ = ['ERRORS']


ERRORS = {
    Topic.DoesNotExist: lambda _: JSONMessage('No such topic.', status=404),
    Response.DoesNotExist: lambda _: JSONMessage(
        'No such response.', status=404
    )
}
