# Property Management API - Technical Documentation

## 1. System Overview
The Property Management API is a RESTful backend service built using Python, Django, and Django REST Framework (DRF). It manages properties, units, members (tenants), and rental contracts with automated business logic.

## 2. Technical Architecture

### 2.1 Backend Stack
- **Framework**: Django 5.2 & Django REST Framework (DRF)
- **Authentication**: JWT (JSON Web Token) via SimpleJWT
- **Database**: SQLite (Development) / Compatible with PostgreSQL/MySQL for Production
- **Language**: Python 3.10+

### 2.2 Domain-Driven Structure
The project is divided into modular Django apps:
- `users`: IAM, staff registration, and JWT authentication.
- `properties`: Core assets (Properties, Units) and tenant entities (Members).
- `contracts`: Transactional logic, contract lifecycle, and date validation.

---

## 3. Database Schema

### 3.1 Entity Relationship Diagram
- **Property**: Basic asset container (`name`, `address`).
- **Unit**: Individual rentable asset belonging to a Property (`unit_number`, `monthly_rent`, `status`).
- **Member**: Tenant information (`full_name`, `email`).
- **Contract**: Transactional link between Member and Unit (`start_date`, `end_date`, `monthly_rent`, `total_value`).

---

## 4. Business Logic & Constraints

### 4.1 Automated Monthly Rent
When creating a contract, if `monthly_rent` is omitted, the system automatically defaults it to the `monthly_rent` defined in the associated `Unit`.

### 4.2 Contract Value Calculation
The `total_value` of a contract is self-calculated at save-time based on the duration (days) relative to a standard month (30.44 days).

### 4.3 Overlap Protection (Concurrency-Safe)
The system prevents double-booking a unit. It validates that no other contract exists for the same unit where:
`ExistingStart < NewEnd AND ExistingEnd > NewStart`.

### 4.4 Unit Status Sync (Dynamic)
- Units automatically calculate their status (`occupied`/`available`) whenever a linked contract is **Saved** or **Deleted**.
- The logic checks for any currently active contract for that specific unit.

---

## 5. API Reference

### 5.1 Authentication
- `POST /api/auth/register/`: Create a staff account.
- `POST /api/auth/login/`: Get `access` and `refresh` tokens.

### 5.2 Properties & Units
- `GET /api/properties/`: List all properties.
- `POST /api/properties/`: Create a new property.
- `POST /api/properties/:id/units/`: Add a unit to a property.
- `GET /api/units/?status=available`: List available units.

### 5.3 Members
- `GET /api/members/`: List registred tenants.
- `POST /api/members/`: Register a new tenant.

### 5.4 Contracts
- `POST /api/contracts/`: Create a contract (checks for overlaps).
- `GET /api/contracts/`: List all contracts.
  - **Optimization**: Uses `select_related('member', 'unit')` to fetch all data in a single SQL join.
  - **Response Helpers**: Includes `member_name` and `unit_number` for immediate UI rendering without extra lookups.
- `GET /api/contracts?active=true`: List only ongoing/active contracts.
- `GET /api/contracts?active=false`: List only inactive (expired or future) contracts.

---

## 6. Development & Hosting

### 6.1 Local Setup
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver`

### 6.2 Testing
Run the automated suite using `pytest`. The system ensures 100% path coverage for the overlapping date logic.
```bash
pytest
```

---

## 7. Postman Collection
A pre-configured collection is included in the project root: `postman_collection.json`. It includes automatic token handling in the Login request "Tests" script.
