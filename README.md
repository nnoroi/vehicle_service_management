# Mercedes Vehicle Service Management System

A web-based vehicle service management system developed as a portfolio project using Python, Flask and SQLite.

The system is a vehicle service management application focused on managing Mercedes-Benz vehicles and their service history. It provides vehicle management, service record management, maintenance tracking and a dashboard for monitoring service activity.

> This is an independent portfolio project and is not an official Mercedes-Benz application.

## Features

### Vehicle Management

* Add new vehicles
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
* Handle missing vehicles and service records
* Return appropriate HTTP error responses for invalid API requests

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
vehicle_service_management/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── validators/
│   ├── static/
│   ├── templates/
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

The application will then be available locally through the Flask development server.

## Running Tests

The project uses pytest for automated testing.

Run the complete test suite with:

```powershell
python -m pytest
```

The tests cover areas including:

* Database functionality
* Vehicle management
* Service record management
* Validation
* Maintenance calculations
* Dashboard functionality
* API routes
* Error handling

## Architecture

The application separates responsibilities into different layers:

```text
Routes
  ↓
Services
  ↓
Database
```

* **Routes** handle HTTP requests and responses.
* **Services** contain application and business logic.
* **Models** represent application data.
* **Validators** handle input validation.
* **Database** contains SQLite connection and database initialisation logic.
* **Templates** provide the web interface.
* **Tests** verify application behaviour.

This structure helps keep the application modular and easier to maintain.

## Future Improvements

Possible future extensions include:

* User authentication and role-based access
* Improved dashboard analytics
* Automated service reminders
* Customer management
* Appointment scheduling
* Deployment to a production environment
* Additional automated and integration tests
