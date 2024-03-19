# Amigo API

## Overview

`amigo-api` is a RESTful backend service designed for a psychological EHR (Electronic Health Record) system. It serves as the core for managing appointments, billing, medical records, and interactions between clinicians and patients in a counseling center environment.

## Features

- **User Management**: Handle both patients and clinicians with distinct roles and permissions.
- **Appointment Scheduling**: Allows clinicians and patients to create, update, and view appointments.
- **Billing System**: Manage billing records, including creating, updating, and retrieving billing information.
- **Medical Records**: Securely store and manage patients' medical records.
- **Notes and Homework**: Clinicians can assign and manage notes or homework for patients.
- **Real-time Chat**: Facilitate communication between clinicians and patients.

## Technology Stack

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: SQL toolkit and ORM for database operations.
- **PostgreSQL**: The database system.
- **Pytest**: For running unit and integration tests.

## Getting Started

### Prerequisites

- Python 3.7+
- pip
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/amigo-api.git
cd amigo-api
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the PostgreSQL database:
- Create a new PostgreSQL database named `amigo_db`.
- Update the database connection string in `app/config.py`.

4. Start the application:
```bash
uvicorn amigo.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing

Run tests using pytest:
```bash
pytest
```


Ensure all tests pass to confirm the application is set up correctly and functioning as expected.

## Documentation

API documentation is available at `http://localhost:8000/docs` when the server is running, thanks to FastAPI's automatic Swagger UI generation.

## License

This project is licensed under the [MIT License](LICENSE).
