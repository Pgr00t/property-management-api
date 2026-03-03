import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from properties.models import Property, Unit, Member
from contracts.models import Contract
from datetime import date, timedelta
from decimal import Decimal

@pytest.fixture
def api_client():
    client = APIClient()
    user = User.objects.create_user(username='contractadmin', password='password123', is_staff=True)
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
class TestContractAPI:
    def setup_method(self):
        self.prop = Property.objects.create(name='P1', address='A1')
        self.unit = Unit.objects.create(property=self.prop, unit_number='101', monthly_rent=1000.00)
        self.member = Member.objects.create(full_name='M1', email='m1@example.com')
        self.url = reverse('contract-list-create')

    def test_create_contract_calculates_total_value(self, api_client):
        # 1-month contract (approx)
        start = date(2025, 1, 1)
        end = date(2025, 1, 31) # 30 days
        data = {
            'member': self.member.id,
            'unit': self.unit.id,
            'start_date': start,
            'end_date': end,
            'monthly_rent': 1000.00
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 201
        contract = Contract.objects.get(pk=response.data['id'])
        # 30 days / 30.44 * 1000 approx 985.55
        assert contract.total_value > 0
        assert contract.unit.status == 'available' # Because test today is not 2025-01-01

    def test_overlapping_contract_fails(self, api_client):
        # Create first contract
        Contract.objects.create(
            member=self.member,
            unit=self.unit,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            monthly_rent=1000
        )
        
        # Overlapping contract
        data = {
            'member': self.member.id,
            'unit': self.unit.id,
            'start_date': date(2025, 1, 15),
            'end_date': date(2025, 2, 15),
            'monthly_rent': 1000
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 400
        assert "This unit is already booked" in str(response.data)

    def test_unit_status_active(self, api_client):
        # Contract active today
        today = date.today()
        data = {
            'member': self.member.id,
            'unit': self.unit.id,
            'start_date': today - timedelta(days=1),
            'end_date': today + timedelta(days=5),
            'monthly_rent': 1000
        }
        api_client.post(self.url, data)
        self.unit.refresh_from_db()
        assert self.unit.status == 'occupied'

    def test_list_active_contracts(self, api_client):
        today = date.today()
        # Active
        Contract.objects.create(
            member=self.member, unit=self.unit,
            start_date=today - timedelta(days=1),
            end_date=today + timedelta(days=5),
            monthly_rent=1000
        )
        # Inactive (future)
        m2 = Member.objects.create(full_name='M2', email='m2@example.com')
        # We need a different unit or dates for no overlap
        prop2 = Property.objects.create(name='P2', address='A2')
        u2 = Unit.objects.create(property=prop2, unit_number='201', monthly_rent=1000)
        Contract.objects.create(
            member=m2, unit=u2,
            start_date=today + timedelta(days=10),
            end_date=today + timedelta(days=20),
            monthly_rent=1000
        )

        # Filter active
        response = api_client.get(self.url, {'active': 'true'})
        assert response.status_code == 200
        data = response.data['results'] if 'results' in response.data else response.data
        assert len(data) == 1
        assert data[0]['member'] == self.member.id
