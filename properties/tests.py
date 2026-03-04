import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from .models import Property, Unit, Member


@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(
        username="testadmin", password="password123", is_staff=True
    )
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestPropertyAPI:
    def test_create_property(self, api_client):
        url = reverse("property-list-create")
        data = {"name": "Sunset Apartments", "address": "123 Main St"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Property.objects.count() == 1

    def test_list_properties(self, api_client):
        Property.objects.create(name="P1", address="A1")
        url = reverse("property-list-create")
        response = api_client.get(url)
        assert response.status_code == 200
        assert (
            len(response.data["results"]) == 1
            if "results" in response.data
            else len(response.data) == 1
        )


@pytest.mark.django_db
class TestUnitAPI:
    def test_create_unit_under_property(self, api_client):
        prop = Property.objects.create(name="P1", address="A1")
        url = reverse("property-unit-create", kwargs={"property_id": prop.id})
        data = {"unit_number": "101", "monthly_rent": "1200.50"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Unit.objects.count() == 1
        unit = Unit.objects.first()
        assert unit.property == prop
        assert unit.status == "available"

    def test_list_units_with_filter(self, api_client):
        prop = Property.objects.create(name="P1", address="A1")
        Unit.objects.create(
            property=prop, unit_number="101", monthly_rent="1000", status="available"
        )
        Unit.objects.create(
            property=prop, unit_number="102", monthly_rent="1000", status="occupied"
        )

        url = reverse("unit-list")
        response = api_client.get(url, {"status": "available"})
        assert response.status_code == 200
        data = response.data["results"] if "results" in response.data else response.data
        assert len(data) == 1
        assert data[0]["unit_number"] == "101"


@pytest.mark.django_db
class TestMemberAPI:
    def test_create_member(self, api_client):
        url = reverse("member-list-create")
        data = {"full_name": "John Doe", "email": "john@example.com"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Member.objects.count() == 1

    def test_list_members(self, api_client):
        Member.objects.create(full_name="Jane", email="jane@example.com")
        url = reverse("member-list-create")
        response = api_client.get(url)
        assert response.status_code == 200
        data = response.data["results"] if "results" in response.data else response.data
        assert len(data) == 1
