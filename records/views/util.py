"""Utility module."""
from django.http import HttpRequest
from django.middleware.csrf import get_token
from rest_framework import decorators, response


@decorators.api_view(['get'])
def csrf_token_view(request: HttpRequest) -> response.Response:
    """Return csrf token."""
    csrf_token = get_token(request)
    return response.Response({'csrfToken': csrf_token})
