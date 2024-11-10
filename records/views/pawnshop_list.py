from rest_framework import generics, permissions, mixins, response
from django.db.models import Q, QuerySet
from records.models import Pawnshop
from records.serializers import PawnshopSerializer
from django.http import HttpRequest
from typing import Any

class PawnshopList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """View to list all pawnshops or create a new pawnshop."""

    queryset = Pawnshop.objects.all().order_by("name")
    serializer_class = PawnshopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self) -> QuerySet:
        """Filter the pawnshops based on query parameters."""
        queryset = super().get_queryset()
        
        # Keyword search for pawnshop name or description
        keyword = self.request.GET.get("keyword")
        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword)
            )
        
        return queryset

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle GET requests to retrieve a list of pawnshops."""
        return self.list(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> response.Response:
        """Handle POST requests to create a new pawnshop."""
        return self.create(request, *args, **kwargs)
