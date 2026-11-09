"""Configuración común de las pruebas: base temporal y datos de ejemplo."""
import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# Tiene que setearse ANTES de importar config, porque Flask-SQLAlchemy crea el
# motor de la base en el momento del import.
_carpeta = tempfile.mkdtemp()
os.environ["DATABASE_URI"] = f"sqlite:///{Path(_carpeta) / 'test.db'}"

import pytest  # noqa: E402

import app as _app_modulo  # noqa: E402, F401  (registra las rutas /api con add_api)
from config import app as aplicacion, db  # noqa: E402
from models import Person, Pizza  # noqa: E402


def _cargar_datos():
    """Tres personas: una con dos pizzas, una con una, y una sin ninguna."""
    sanchez = Person(lname="Sanchez", fname="Ricardo")
    sanchez.pizzas.append(Pizza(content="Pizza Mozzarella", price=8500.0, size="grande"))
    sanchez.pizzas.append(Pizza(content="Pizza Cebolla", price=7200.0, size="mediana"))

    gomez = Person(lname="Gomez", fname="Cintya")
    gomez.pizzas.append(Pizza(content="Pizza Pepperoni", price=7800.0, size="mediana"))

    lopez = Person(lname="Lopez", fname="Raul")

    db.session.add_all([sanchez, gomez, lopez])
    db.session.commit()


@pytest.fixture
def cliente():
    """Cliente de pruebas de Flask con la base recreada y cargada de cero."""
    with aplicacion.app_context():
        db.drop_all()
        db.create_all()
        _cargar_datos()

        yield aplicacion.test_client()

        db.session.remove()
        db.drop_all()