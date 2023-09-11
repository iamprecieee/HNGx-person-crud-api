# Person CRUD REST API

A simple REST API for performing CRUD operations on person records using Flask-smorest and SQLAlchemy.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation-and-configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed.
- `virtualenv` installed (optional but recommended for isolating project dependencies).
- Git installed.
- Access to a PostgreSQL, MySQL, or SQLite database (SQLite is used by default).

## Installation and Configuration

1. Clone this repository:

   ```
   git clone https://github.com/your-username/person-crud-api.git
   cd person-crud-api

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   ```

   For macOS / Linux:
   ```
   source venv/bin/activate
   ```
   For Windows:
   ```
   venv\Scripts\activate
   ```

4. Install project dependencies:

    ```
   pip install -r requirements.txt
    ```

6. Create a `.flaskenv` file in the root directory for basic environmental variables:
    ```
    DATABASE_URL=sqlite:///data.db  # Use your database URL (e.g., PostgreSQL or MySQL)
    FLASK_ENV=development
    FLASK_APP=app.py
    ```
P.S.: Not recommended for production.

## Database Setup

Create the initial database tables:
    ```
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

## Running The Application

Start the development server using the command:
    ```
    flask run
    ```
    
The API will be running locally at `http://localhost:5000`.
