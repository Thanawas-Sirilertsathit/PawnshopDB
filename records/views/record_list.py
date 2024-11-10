from rest_framework import generics, permissions, mixins, response
from django.db.models import Q, QuerySet
from records.models import Record
from records.serializers import RecordSerializer
from django.http import HttpRequest
from typing import Any

class RecordList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """View to list all records or create a new record."""

    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Filter records based on pawnshop_id and query parameters."""
        # Get all records and order by creation date, descending
        queryset = Record.objects.all().order_by("-start_date")

        # Filter by pawnshop if pawnshop_id is provided
        pawnshop_id = self.request.GET.get("pawnshop_id")
        if pawnshop_id:
            queryset = queryset.filter(pawnshop__id=pawnshop_id)

        # Keyword search for records by name or description
        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            )

        # Filter by a date range if provided
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(start_date__lte=end_date)

        return queryset

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle GET requests to retrieve a list of records."""
        return self.list(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle POST requests to create a new record."""
        return self.create(request, *args, **kwargs)
