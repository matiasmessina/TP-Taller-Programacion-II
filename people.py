from config import db
from flask import abort
from models import Person, people_schema, person_schema, pizzas_schema


def read_all():
    people = Person.query.all()
    return people_schema.dump(people)


def create(person):
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with last name {lname} already exists")


def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with last name {lname} not found")


def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 200
    else:
        abort(404, f"Person with last name {lname} not found")


def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return "", 204
    else:
        abort(404, f"Person with last name {lname} not found")

def read_pizzas(lname):
    """Devuelve solo las pizzas de una persona."""
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is None:
        abort(404, f"No existe una persona con el apellido {lname}")

    return pizzas_schema.dump(person.pizzas)


def read_resumen(lname):
    """Devuelve cuántas pizzas pidió una persona y cuánto gastó en total."""
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is None:
        abort(404, f"No existe una persona con el apellido {lname}")

    return {
        "lname": person.lname,
        "fname": person.fname,
        "cantidad_pizzas": len(person.pizzas),
        "total_gastado": round(sum(pizza.price for pizza in person.pizzas), 2),
    }
