# MyMechanicShop

MyMechanicShop is a Flask-based web application designed to manage a mechanic shop's operations. It provides functionality for managing customers, mechanics, service tickets, and their relationships. The app uses SQLAlchemy for database management and Marshmallow for data serialization and validation.

---

## Features

- **Customer Management**:
  - Add, update, delete, and retrieve customer details.
- **Mechanic Management**:
  - Add, update, delete, and retrieve mechanic details.
- **Service Ticket Management**:
  - Create service tickets, assign mechanics, remove mechanics, and retrieve service tickets.
- **Blueprint Architecture**:
  - Organized using Flask Blueprints for modularity.
- **Database Integration**:
  - SQLAlchemy ORM for database operations.
- **Validation**:
  - Marshmallow schemas for data validation and serialization.

---

## Project Structure
MyMechanicShop/ ├── App/ │ ├── init.py # Application factory and blueprint registration │ ├── config.py # Configuration settings (e.g., DevelopmentConfig) │ ├── extensions.py # Flask extensions (SQLAlchemy, Marshmallow) │ ├── models.py # SQLAlchemy models for database tables │ ├── schemas.py # Marshmallow schemas for serialization/validation │ ├── routes.py # General routes for the app │ ├── Blueprints/ │ │ ├── Mechanic_blueprint/ │ │ │ ├── init.py # Mechanic blueprint initialization │ │ │ ├── routes.py # Routes for managing mechanics │ │ ├── Service_Ticket_blueprint/ │ │ │ ├── init.py # Service ticket blueprint initialization │ │ │ ├── routes.py # Routes for managing service tickets │ │ ├── Members_blueprint/ │ │ │ ├── init.py # Customer blueprint initialization │ │ │ ├── routes.py # Routes for managing customers ├── run.py # Entry point for running the Flask app ├── requirements.txt # Python dependencies ├── README.md # Project documentation └── .venv/ # Virtual environment (not included in version control)

Set Up a Virtual Environment:

---

## Installation

### Prerequisites
- Python 3.9 or higher
- MySQL or another supported database
- `pip` (Python package manager)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/MyMechanicShop.git
   cd MyMechanicShop

Install Dependencies: pip install -r requirements.txt

Set Up the Database: SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/mymechanicshop'

Update the SQLALCHEMY_DATABASE_URI in config.py to match your database credentials:
Create the database tables:
Run the Application:

Access the Application: Open your browser and navigate to:

API Endpoints
Customers
POST /customers: Add a new customer.
GET /customers: Retrieve all customers.
GET /customers/<customer_id>: Retrieve a specific customer.
PUT /customers/<customer_id>: Update a customer's details.
DELETE /customers/<customer_id>: Delete a customer.
Mechanics
POST /mechanics: Add a new mechanic.
GET /mechanics: Retrieve all mechanics.
GET /mechanics/<mechanic_id>: Retrieve a specific mechanic.
PUT /mechanics/<mechanic_id>: Update a mechanic's details.
DELETE /mechanics/<mechanic_id>: Delete a mechanic.
Service Tickets
POST /service_tickets: Create a new service ticket.
GET /service_tickets: Retrieve all service tickets.
PUT /service_tickets/<ticket_id>/assign-mechanic/<mechanic_id>: Assign a mechanic to a service ticket.
PUT /service_tickets/<ticket_id>/remove-mechanic/<mechanic_id>: Remove a mechanic from a service ticket.
Configuration
The application uses a DevelopmentConfig class for configuration. Update the config.py file to customize settings:

Testing
To test the API, you can use tools like: class DevelopmentConfig: Update the config.py file to customize settings:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/mymechanicshop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

Testing
To test the API, you can use tools like:

Postman: Create requests to test the endpoints.
cURL: Use the command line to send HTTP requests.
Example: curl -X POST http://127.0.0.1:5000/customers \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "email": "john@example.com", "address": "123 Main St", "phone": "555-1234"}'

Postman: Create requests to test the endpoints.
cURL: Use the command line to send HTTP requests.
Example:

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch:
Commit your changes:
Push to your branch:
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Flask for providing a lightweight and flexible web framework.
SQLAlchemy for database management.
Marshmallow for data serialization and validation.


---

### Steps to Save:
1. Copy the content above.
2. Paste it into your `README.md` file.
3. Save the file.

Let me know if you need further assistance!
---

