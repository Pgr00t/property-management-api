from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Property, Unit, Member
from .serializers import PropertySerializer, UnitSerializer, MemberSerializer

from rest_framework import filters


class PropertyListCreateView(generics.ListCreateAPIView):
    """
    GET /api/properties
    POST /api/properties
    """

    queryset = Property.objects.prefetch_related("units").all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "address"]
    ordering_fields = ["name", "id"]
    ordering = ["-id"]

    def get_serializer_class(self):
        return PropertySerializer


class PropertyDetailView(generics.RetrieveAPIView):
    """
    GET /api/properties/:property_id
    """

    queryset = Property.objects.prefetch_related("units").all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]


class PropertyUnitCreateView(generics.CreateAPIView):
    """
    POST /api/properties/:property_id/units
    """

    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        property_obj = get_object_or_404(Property, pk=self.kwargs.get("property_id"))
        serializer.save(property=property_obj)


class UnitListView(generics.ListAPIView):
    """
    GET /api/units (support ?status=available filtering)
    """

    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["monthly_rent", "unit_number", "id"]
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Unit.objects.select_related("property").all()
        status = self.request.query_params.get("status", None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset


class MemberListCreateView(generics.ListCreateAPIView):
    """
    GET /api/members
    POST /api/members
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["full_name", "email"]
    ordering_fields = ["full_name", "id"]
    ordering = ["-id"]
