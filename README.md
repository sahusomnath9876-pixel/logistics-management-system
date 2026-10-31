# Logistics Management System

A backend-focused Logistics Management System built with Python, MySQL,
SQLAlchemy, and a layered architecture.

The project was designed to practice real-world backend development
concepts such as authentication, business logic separation, database
operations, repository/service architecture, transaction handling, and
automated testing.

## Features

-   User authentication and password hashing
-   Role-based access control
-   Customer management
-   Product management
-   Inventory management
-   Warehouse management
-   Order management
-   Payment management
-   Delivery-time calculation
-   MySQL database integration
-   SQLAlchemy ORM
-   Environment-based configuration
-   Automated tests with pytest
-   Repository and service layer separation
-   Error handling and database transaction management

## Architecture

The project follows a layered backend architecture:

``` text
Client / Main Program
        ↓
     Services
        ↓
   Repositories
        ↓
     Models
        ↓
 SQLAlchemy / MySQL
```

### Main Layers

**Services**

Contains business logic and coordinates application operations.

``` text
app/services/
├── auth_service.py
├── customer_service.py
├── order_service.py
├── payment_service.py
├── product_service.py
└── warehouse_services.py
```

**Repositories**

Handles database-related operations and keeps database access separate
from business logic.

``` text
app/repositories/
├── customer_repo.py
├── delivery_time.py
├── inventory_repo.py
├── orders_repo.py
└── user_repo.py
```

**Models**

Contains SQLAlchemy database models representing the application's data
structures.

**Database**

Contains database connection and session management.

**Tests**

Contains automated tests for the application's major services and
workflows.

## Project Structure

``` text
Logistics Management Project/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   │   ├── customer_repo.py
│   │   ├── delivery_time.py
│   │   ├── inventory_repo.py
│   │   ├── orders_repo.py
│   │   └── user_repo.py
│   │
│   └── services/
│       ├── auth_service.py
│       ├── customer_service.py
│       ├── order_service.py
│       ├── payment_service.py
│       ├── product_service.py
│       └── warehouse_services.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_customer.py
│   ├── test_order.py
│   ├── test_payment.py
│   ├── test_product.py
│   └── test_warehouse.py
│
├── .env
├── .gitignore
├── development_plans.txt
└── requirements.txt
```

## Technologies Used

-   **Python** --- application and business logic
-   **MySQL** --- relational database
-   **SQLAlchemy** --- ORM and database interaction
-   **PyMySQL** --- MySQL database driver
-   **bcrypt** --- password hashing
-   **python-dotenv** --- environment variable management
-   **geopy** --- geocoding and location-related functionality
-   **requests** --- HTTP/API requests
-   **pytest** --- automated testing

## Authentication

The authentication system uses password hashing with `bcrypt`.

The general authentication flow is:

``` text
User Credentials
       ↓
Authentication Service
       ↓
Password Verification
       ↓
User / Role Validation
       ↓
Authorized Operation
```

Passwords are not stored as plain text.

## Testing

The project uses `pytest` for automated testing.

Test modules cover major application areas:

``` text
tests/
├── test_auth.py
├── test_customer.py
├── test_order.py
├── test_payment.py
├── test_product.py
└── test_warehouse.py
```

Run the complete test suite:

``` bash
python -m pytest -v
```

Run a specific test file:

``` bash
python -m pytest tests/test_auth.py -v
```

For example:

``` bash
python -m pytest tests/test_customer.py -v
```

## Installation

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Logistics Management Project"
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

Activate it on Windows:

``` bash
venv\Scripts\activate
```

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 4. Configure the database

Create a MySQL database and configure the required database credentials
in a `.env` file.

Example:

``` env
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

Use the variable names expected by the project's database configuration.

### 5. Run the application

``` bash
python main.py
```

## Environment Variables

Sensitive configuration should be stored in `.env` and should not be
committed to GitHub.

A `.env.example` file can be used to show the required configuration
without exposing real credentials.

Example:

``` env
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

## What I Learned From This Project

This project was built as a practical backend development project rather
than only as a collection of tutorials.

Key concepts practiced include:

-   Object-oriented Python
-   Layered application architecture
-   Repository pattern
-   Service layer design
-   SQLAlchemy ORM
-   MySQL database design
-   Authentication and authorization
-   Password hashing
-   Environment variables
-   Database transactions
-   Exception handling
-   External API usage
-   Automated testing with pytest
-   Project organization and separation of concerns

## Future Improvements

Possible future improvements include:

-   REST API using FastAPI
-   Frontend interface
-   Advanced order tracking
-   Delivery-agent management
-   Notifications
-   Improved reporting and analytics
-   Deployment to a cloud platform

> FastAPI is intentionally not part of the current version. It is being
> explored separately in a dedicated API project so that this project
> remains focused on its original backend architecture.

## Project Status

**Completed --- Version 1**

The core backend functionality, database integration, service/repository
architecture, authentication, and automated tests have been implemented.

## Author

**Somnath Sahu**

This project was created as part of my journey toward becoming a
professional Python backend developer.
