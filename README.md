# Property Management API

A RESTful API for managing properties, units, members, and rental contracts. Built with Python, Django, and Django REST Framework.

## Features

- **Authentication**: JWT-based authentication for staff users.
- **Properties**: Create and manage properties and their units.
- **Members**: Register tenants/members.
- **Contracts**: 
  - Automated calculation of total contract value.
  - Prevention of double-booking (overlapping dates for the same unit).
  - Automatic unit status updates (Available/Occupied).
  - Querying active contracts.

## Setup Instructions

### Prerequisites
- Python 3.9+
- Pip

### 1. Clone the repository
```bash
git clone <repo-url>
cd property_management_api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (Optional, for admin access)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

## Running Tests
To run the automated test suite:
```bash
pytest
```

## API Documentation

### Auth
- `POST /api/auth/register/`: Register a new staff user.
- `POST /api/auth/login/`: Obtain JWT tokens (Access & Refresh).

### Properties & Units
- `POST /api/properties/`: Create a property.
- `GET /api/properties/`: List all properties.
- `GET /api/properties/:id/`: Retrieve property details.
- `POST /api/properties/:id/units/`: Create a unit under a property.
- `GET /api/units/`: List units (Filter by `?status=available` or `?status=occupied`).

### Members
- `POST /api/members/`: Register a new member.
- `GET /api/members/`: List members.

### Contracts
- `POST /api/contracts/`: Create a rental contract.
- `GET /api/contracts/`: List all contracts.
- `GET /api/contracts?active=true`: List only active contracts.

## Sample Responses

### Property Response
```json
{
    "id": 1,
    "name": "Ocean View",
    "address": "123 Coastal Loop",
    "units": [
        {
            "id": 1,
            "property": 1,
            "property_name": "Ocean View",
            "unit_number": "A-101",
            "monthly_rent": "2000.00",
            "status": "occupied"
        }
    ]
}
```

### Unit Response
```json
{
    "id": 1,
    "property": 1,
    "property_name": "Ocean View",
    "unit_number": "A-101",
    "monthly_rent": "2000.00",
    "status": "occupied"
}
```

### Member Response
```json
{
    "id": 1,
    "full_name": "John Postman",
    "email": "john@postman.com"
}
```

### Contract Response
```json
{
    "id": 1,
    "member": 1,
    "member_name": "John Doe",
    "unit": 1,
    "unit_number": "101",
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "monthly_rent": "1000.00",
    "total_value": "985.55"
}
```
