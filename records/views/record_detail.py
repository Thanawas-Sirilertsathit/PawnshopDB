from rest_framework import generics, permissions, response
from django.http import HttpRequest
from records.models import Record
from records.serializers import RecordSerializer
from typing import Any

class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a specific record."""

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle GET request to retrieve a specific record."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle PUT request to update a specific record."""
        return self.update(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle DELETE request to delete a specific record."""
        return self.destroy(request, *args, **kwargs)
