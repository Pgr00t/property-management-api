from django.urls import path
from .views import (
    PropertyListCreateView,
    PropertyDetailView,
    PropertyUnitCreateView,
    UnitListView,
    MemberListCreateView,
)

urlpatterns = [
    path("properties/", PropertyListCreateView.as_view(), name="property-list-create"),
    path("properties/<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
    path(
        "properties/<int:property_id>/units/",
        PropertyUnitCreateView.as_view(),
        name="property-unit-create",
    ),
    path("units/", UnitListView.as_view(), name="unit-list"),
    path("members/", MemberListCreateView.as_view(), name="member-list-create"),
]
