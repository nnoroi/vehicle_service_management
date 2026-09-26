# Mercedes Vehicle Service Management System

A web-based vehicle service management system developed as a portfolio project using Python, Flask and SQLite.

The application is focused on managing Mercedes-Benz vehicles, their service records and maintenance information. It provides vehicle management, service record management, maintenance tracking, dashboard monitoring and a REST API.

> This is an independent portfolio project and is not an official Mercedes-Benz application.

**GitHub:** https://github.com/nnoroi/vehicle_service_management

## Features

### Vehicle Management

* Add new Mercedes-Benz vehicles
* View vehicle details
* Edit vehicle information
* Delete vehicles
* Track mileage, registration, VIN and fuel type
* View a vehicle's service history

### Service Record Management

* Create service records
* View individual service records
* Edit service records
* Delete service records
* Track service type, date, mileage, cost and status
* Add notes to service records

### Maintenance Tracking

* Calculate the next recommended service mileage
* Determine whether a vehicle is due for service
* Display miles remaining until the next service
* Identify vehicles requiring maintenance
* Prevent service mileage from moving backwards

### Dashboard

* Total number of vehicles
* Total number of service records
* Number of vehicles requiring service
* List of vehicles currently needing service
* Recent service activity
* Service status indicators

### Validation and Error Handling

* Validate vehicle and service record input
* Prevent invalid mileage and cost values
* Validate service record status
* Validate service mileage chronology
* Handle missing vehicles and service records
* Handle missing and malformed JSON requests
* Return appropriate HTTP error responses
* Use a global Flask error handler for `ValueError` exceptions

## Technologies

* **Python**
* **Flask**
* **SQLite**
* **HTML**
* **CSS**
* **Jinja2**
* **pytest**
* **Git / GitHub**

## Project Structure
```text
├── app/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── validators/
│   ├── utils/
│   ├── static/
│   ├── templates/
│   ├── errors.py
│   └── __init__.py
│
├── tests/
│
├── instance/
│   └── database.db
│
├── .gitignore
├── README.md
└── requirements.txt
```

The application code is organised into separate modules based on their responsibilities.

The local SQLite database is stored in `instance/` and is excluded from version control.

## Architecture

The application uses a layered structure to separate HTTP handling, business logic, validation and database operations.

                    ┌──────────────┐
                    │    Routes    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Services   │
                    └───┬──────┬───┘
                        │      │
              ┌─────────┘      └─────────┐
              ▼                          ▼
       ┌─────────────┐            ┌─────────────┐
       │ Validators  │            │   Mappers   │
       └─────────────┘            └─────────────┘
              │                          │
              └────────────┬─────────────┘
                           ▼
                    ┌──────────────┐
                    │   Database   │
                    │    SQLite    │
                    └──────────────┘

## Application Layers

* Routes handle HTTP requests, responses and page rendering.
* Services contain the application's business and database-related logic.
* Models represent application data such as vehicles and service records.
* Validators check user input before data is saved or updated.
* Mappers convert database rows into model objects and models into API  responses.
* Database provides SQLite connections and database initialisation.
* Templates provide the web interface using HTML and Jinja2.
* Utils contain reusable application utilities such as date formatting.
* Tests verify application behaviour and help prevent regressions.
* Error handling provides consistent responses for application errors.

This separation keeps the application modular, easier to test and easier to maintain.

## REST API

The application provides REST API endpoints for vehicle and service record management.

### Vehicles

| Method | Endpoint                             | Description                         |
| ------ | ------------------------------------ | ----------------------------------- |
| GET    | `/vehicles`                          | Display the vehicle management page |
| POST   | `/vehicles`                          | Create a vehicle through the API    |
| GET    | `/vehicles/<vehicle_id>`             | View vehicle details                |
| PUT    | `/vehicles/<vehicle_id>`             | Update a vehicle                    |
| DELETE | `/vehicles/<vehicle_id>`             | Delete a vehicle                    |
| GET    | `/vehicles/<vehicle_id>/maintenance` | Get maintenance information         |

### Service Records

| Method | Endpoint                          | Description                       |
| ------ | --------------------------------- | --------------------------------- |
| GET    | `/services`                       | Display service records           |
| GET    | `/vehicles/<vehicle_id>/services` | Get service records for a vehicle |
| POST   | `/vehicles/<vehicle_id>/services` | Create a service record           |
| GET    | `/services/<service_id>`          | Get a service record              |
| PUT    | `/services/<service_id>`          | Update a service record           |
| DELETE | `/services/<service_id>`          | Delete a service record           |

API requests use JSON where applicable.

Example vehicle creation request:

```json
{
    "make": "Mercedes-Benz",
    "model": "C-Class",
    "year": 2022,
    "registration": "MJ22 XTR",
    "vin": "W1K2060421F123456",
    "mileage": 38450,
    "fuel_type": "Petrol"
}
```

Successful API requests return JSON responses, while invalid requests return appropriate HTTP status codes and JSON error messages.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/nnoroi/vehicle_service_management.git
cd vehicle_service_management
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Initialise the database

```powershell
python -m app.database.init_db
```

### 6. Run the application

```powershell
flask --app app run
```

The application will then be available through the Flask development server.

## Running Tests

The project uses **pytest** for automated testing.

Run the complete test suite with:

```powershell
python -m pytest
```

The test suite covers areas including:

* Database functionality
* Vehicle management
* Service record management
* Input validation
* Maintenance calculations
* Service history
* Dashboard functionality
* API routes
* Error handling
* Invalid and missing API input
* Service mileage integrity

Tests use isolated database connections and mocking where required to avoid modifying the application's local database.

## Screenshots

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Vehicle Management

![Vehicles](screenshots/vehicles.png)

![Vehicle Details](screenshots/vehicle-details.png)

### Service Management

![Service History](screenshots/service-history.png)

![Add Service](screenshots/add-service.png)

![Service Details](screenshots/service-details.png)

### Testing

![Tests](screenshots/tests.png)

## Development Approach

The project was developed incrementally using Git and feature branches.

Development focused on:

* Separating business logic from routes
* Reusable validation
* Automated testing
* Small, logically complete Git commits
* API error handling
* Maintaining data integrity
* Building a clear and maintainable application structure

## Future Improvements

Possible future extensions include:

* User authentication and role-based access
* Improved dashboard analytics
* Automated service reminders
* Customer management
* Appointment scheduling
* Deployment to a production environment
* Additional integration tests
* API documentation using OpenAPI/Swagger
