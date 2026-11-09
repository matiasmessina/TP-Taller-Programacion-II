from config import db
from flask import abort
from models import Pizza, Person, pizza_schema, pizzas_schema


def read_all(person_id=None):
    """Devuelve todas las pizzas, o solo las de una persona si llega person_id."""
    if person_id is None:
        pizzas = Pizza.query.order_by(Pizza.timestamp.desc()).all()
        return pizzas_schema.dump(pizzas)

    person = db.session.get(Person, person_id)

    if person is None:
        abort(404, f"No existe una persona con el ID {person_id}")

    return pizzas_schema.dump(person.pizzas)

def read_one(pizza_id):
    pizza = db.session.get(Pizza, pizza_id)

    if pizza is not None:
        return pizza_schema.dump(pizza)
    else:
        abort(404, f"Pizza with ID {pizza_id} not found")


def update(pizza_id, pizza):
    existing_pizza = db.session.get(Pizza, pizza_id)

    if existing_pizza:
        update_pizza = pizza_schema.load(pizza, session=db.session)
        existing_pizza.content = update_pizza.content
        existing_pizza.price = update_pizza.price
        existing_pizza.size = update_pizza.size
        db.session.merge(existing_pizza)
        db.session.commit()
        return pizza_schema.dump(existing_pizza), 200
    else:
        abort(404, f"Pizza with ID {pizza_id} not found")


def delete(pizza_id):
    existing_pizza = db.session.get(Pizza, pizza_id)

    if existing_pizza:
        db.session.delete(existing_pizza)
        db.session.commit()
        return "", 204
    else:
        abort(404, f"Pizza with ID {pizza_id} not found")


def create(pizza):
    person_id = pizza.get("person_id")
    person = db.session.get(Person, person_id)

    if person:
        new_pizza = pizza_schema.load(pizza, session=db.session)
        person.pizzas.append(new_pizza)
        db.session.commit()
        return pizza_schema.dump(new_pizza), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")
