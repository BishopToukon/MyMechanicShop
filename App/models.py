from sqlalchemy import Table, Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List
from App.extensions import db  
from werkzeug.security import generate_password_hash, check_password_hash



# Junction Table
service_mechanics = Table(
    "service_mechanics",
    db.metadata,
    Column("ticket_id", ForeignKey("service_ticket.ticket_id"), primary_key=True),
    Column("mechanic_id", ForeignKey("mechanics.mechanic_id"), primary_key=True)
)

inventory_tickets = Table(
    "inventory_tickets",
    db.metadata,
    Column("ticket_id", ForeignKey("service_ticket.ticket_id"), primary_key=True),
    Column("item_id", ForeignKey("inventory.item_id"), primary_key=True)
)

class Customer(db.Model):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    tickets: Mapped[List["ServiceTicket"]] = relationship(
    "ServiceTicket",
    back_populates="customer",
    cascade="all, delete-orphan"
)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    ticket_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"), nullable=False)

    # Relationship back to Customer
    customer: Mapped["Customer"] = relationship(
        "Customer",
        back_populates="tickets"
    )

    # Many-to-many relationship with Mechanics
    mechanics: Mapped[List["Mechanics"]] = relationship(
        "Mechanics",
        secondary=service_mechanics,
        back_populates="tickets"
    )

    # Define the inventory_items relationship
    inventory_items: Mapped[List["Inventory"]] = relationship(
        "Inventory",
        secondary=inventory_tickets,
        back_populates="service_tickets"
    )


class Mechanics(db.Model):
    __tablename__ = "mechanics"

    mechanic_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
#
    tickets: Mapped[List["ServiceTicket"]] = relationship(
        "ServiceTicket",
        secondary=service_mechanics,
        back_populates="mechanics"
    )

class Inventory(db.Model):
    __tablename__ = "inventory"

    item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Define the service_tickets relationship
    service_tickets: Mapped[List["ServiceTicket"]] = relationship(
        "ServiceTicket",
        secondary=inventory_tickets,
        back_populates="inventory_items"
    )