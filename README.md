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
- **Flask-Limiter**: Rate limiting for API endpoints.
- **Flask-Caching**: Caching for optimized performance.

---

## API Endpoints

### **Service Tickets**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/tickets/`                       | Create a new service ticket.             |
| `GET`       | `/tickets/`                       | Get all service tickets (paginated).     |
| `PUT`       | `/tickets/<ticket_id>/edit`       | Add or remove mechanics from a ticket.   |

### **Mechanics**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/mechanics/`                     | Create a new mechanic.                   |
| `GET`       | `/mechanics/most-tickets`         | Get mechanics ordered by ticket count.   |

### **Customers**
| HTTP Method | Endpoint                          | Description                              |
|-------------|-----------------------------------|------------------------------------------|
| `POST`      | `/customers/`                     | Create a new customer.                   |
| `GET`       | `/customers/`                     | Get all customers (paginated).           |

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

### Prerequisites
- Python 3.9 or higher
- MySQL or another supported database
- `pip` (Python package manager)

Directory Structure
MyMechanicShop/
├── App/
│   ├── Blueprints/
│   │   ├── Inventory/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   ├── Mechanic_blueprint/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   ├── Service_Ticket_blueprint/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   ├── extensions.py
│   ├── models.py
│   ├── __init__.py
├── requirements.txt
├── run.py
├── README.mdMyMechanicShop/
├── App/
│   ├── Blueprints/
│   │   ├── Inventory/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   ├── Mechanic_blueprint/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   │   ├── Service_Ticket_blueprint/
│   │   │   ├── routes.py
│   │   │   ├── schemas.py
│   ├── extensions.py
│   ├── models.py
│   ├── __init__.py
├── requirements.txt
├── run.py
├── README.md

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

