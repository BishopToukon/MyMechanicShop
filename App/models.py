from sqlalchemy import Table, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List
from App.extensions import db   



# Junction Table
service_mechanics = Table(
    "service_mechanics",
    db.metadata,
    Column("ticket_id", ForeignKey("service_ticket.ticket_id"), primary_key=True),
    Column("mechanic_id", ForeignKey("mechanics.mechanic_id"), primary_key=True),
)


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)

    cars: Mapped[List["Cars"]] = relationship(
        "Cars",
        back_populates="owner",
        cascade="all, delete-orphan"
    )


class Cars(db.Model):
    __tablename__ = "cars"

    vin: Mapped[str] = mapped_column(String(17), primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id"))

    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    owner: Mapped["Customer"] = relationship("Customer", back_populates="cars")

    tickets: Mapped[List["ServiceTicket"]] = relationship(
        "ServiceTicket",
        back_populates="car",
        cascade="all, delete-orphan"
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    ticket_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    vin: Mapped[str] = mapped_column(
        String(17),
        ForeignKey("cars.vin"),
        nullable=False
    )

    description: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    car: Mapped["Cars"] = relationship(
        "Cars",
        back_populates="tickets"
    )

    mechanics: Mapped[List["Mechanics"]] = relationship(
        "Mechanics",
        secondary=service_mechanics,
        back_populates="tickets"
    )


class Mechanics(db.Model):
    __tablename__ = "mechanics"

    mechanic_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = relationship(
        "ServiceTicket",
        secondary=service_mechanics,
        back_populates="mechanics"
    )
