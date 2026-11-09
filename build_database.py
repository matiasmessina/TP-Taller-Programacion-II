from datetime import datetime

from config import app, db
from models import Pizza, Person

PEOPLE_PIZZA = [
    {
        "lname": "Sanchez",
        "fname": "Ricardo",
        "pizzas": [
            ("Pizza Mozzarella y Queso", 8500.0, "grande", "2022-01-06 17:10:24"),
            ("Pizza Cebolla y Queso", 7200.0, "mediana", "2022-03-05 22:17:54"),
            ("Pizza Roquefort", 9100.0, "grande", "2022-03-05 22:18:10"),
        ],
    },
    {
        "lname": "Gomez",
        "fname": "Cintya",
        "pizzas": [
            ("Pizza Pepperoni", 7800.0, "mediana", "2022-01-01 09:15:03"),
            ("Pizza de Jamón Crudo y Rúcula", 9500.0, "grande", "2022-02-06 13:09:21"),
        ],
    },
    {
        "lname": "Lopez",
        "fname": "Raul",
        "pizzas": [
            ("Pizza Arrollada", 6400.0, "chica", "2022-01-07 22:47:54"),
            ("Pizza Cuatro Quesos", 8900.0, "mediana", "2022-01-07 22:47:54"),
        ],
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in PEOPLE_PIZZA:
        new_person = Person(lname=data.get("lname"), fname=data.get("fname"))
        for content, price, size, timestamp in data.get("pizzas", []):
            new_person.pizzas.append(
                Pizza(
                    content=content,
                    price=price,
                    size=size,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )
        db.session.add(new_person)
    db.session.commit()