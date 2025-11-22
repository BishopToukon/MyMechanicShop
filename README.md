# MyMechanicShop

MyMechanicShop is a Flask-based web application designed to manage service tickets, mechanics, customers, and inventory for a mechanic shop. It provides a RESTful API for managing these entities with CRUD operations and additional functionality.

---

## Features

### 1. **Service Tickets**
- Create, read, update, and delete service tickets.
- Assign and remove mechanics from service tickets.
- Paginate service tickets for efficient data retrieval.

### 2. **Mechanics**
- Create, read, update, and delete mechanics.
- Retrieve mechanics ordered by the number of tickets they have worked on.

### 3. **Customers**
- Create, read, update, and delete customers.
- Paginate customer data for efficient retrieval.

### 4. **Inventory**
- Create, read, update, and delete inventory items.
- Manage parts stored in the inventory.

---

## Technologies Used

- **Flask**: Lightweight and flexible web framework.
- **SQLAlchemy**: ORM for database management.
- **Marshmallow**: Data serialization and validation.
- **Flask-Swagger**: API documentation.
- **Flask-Swagger-UI**: Interactive API documentation.
- **Flask-Limiter**: Rate limiting for API endpoints.
- **Flask-Caching**: Caching for optimized performance.
- **unittest**: Built-in Python library for testing.

---

## API Endpoints

### **Service Tickets**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/tickets/`                       | Create a new service ticket.             |
| `GET`       | `/tickets/`                       | Get all service tickets (paginated).     |
| `PUT`       | `/tickets/<ticket_id>/edit`       | Add or remove mechanics from a ticket.   |
| `DELETE`    | `/tickets/<ticket_id>`            | Delete a service ticket.                 |

### **Mechanics**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/mechanics/`                     | Create a new mechanic.                   |
| `GET`       | `/mechanics/`                     | Get all mechanics.                       |
| `GET`       | `/mechanics/most-tickets`         | Get the mechanic with the most tickets.  |
| `PUT`       | `/mechanics/<mechanic_id>`        | Update a mechanic.                       |
| `DELETE`    | `/mechanics/<mechanic_id>`        | Delete a mechanic.                       |

### **Customers**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/customers/`                     | Create a new customer.                   |
| `GET`       | `/customers/`                     | Get all customers (paginated).           |
| `GET`       | `/customers/<customer_id>`        | Get a specific customer.                 |
| `PUT`       | `/customers/<customer_id>`        | Update a customer.                       |
| `DELETE`    | `/customers/<customer_id>`        | Delete a customer.                       |

### **Inventory**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/inventory/`                     | Create a new inventory item.             |
| `GET`       | `/inventory/`                     | Get all inventory items.                 |
| `GET`       | `/inventory/<item_id>`            | Get a specific inventory item.           |
| `PUT`       | `/inventory/<item_id>`            | Update an inventory item.                |
| `DELETE`    | `/inventory/<item_id>`            | Delete an inventory item.                |

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/MyMechanicShop.git
   cd MyMechanicShop
```

API Documentation
The API is documented using Swagger and Flask-Swagger-UI. You can access the interactive API documentation at:

The swagger.yaml file contains detailed documentation for each route, including:

Path, endpoint, and HTTP method.
Tags, summaries, and descriptions.
Parameters for POST and PUT requests.
Responses with examples.
Definitions for request payloads and responses.
Testing
Test Suite:

The project includes a comprehensive test suite using Python’s unittest library.
Test files are located in the tests folder and include:
test_inventory.py
test_mechanics.py
test_customers.py
test_service_ticket.py
Run Tests: To run the tests, use the following command:

Test Coverage:

Positive tests ensure routes work as expected with valid input.
Negative tests handle invalid input and edge cases.
Example Requests
Create an Inventory Item
Request: pytest

Test Coverage:

Positive tests ensure routes work as expected with valid input.
Negative tests handle invalid input and edge cases.
Example Requests
Create an Inventory Item
Request: curl -X POST http://127.0.0.1:5000/inventory/ \
-H "Content-Type: application/json" \
-d '{
    "item_name": "Brake Pads",
    "quantity": 50,
    "price": 25.99
}'

Response: {
    "message": "Inventory item created successfully",
    "data": {
        "item_id": 1,
        "item_name": "Brake Pads",
        "quantity": 50,
        "price": 25.99
    }
}