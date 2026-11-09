"""Pruebas de la API REST de Personas y Pizzas."""


def _id_de(cliente, lname):
    """Busca el id de una persona por su apellido, sin depender del autoincremental."""
    return cliente.get(f"/api/people/{lname}").get_json()["id"]


# --------------------------- Personas ---------------------------

def test_listar_personas(cliente):
    respuesta = cliente.get("/api/people")
    assert respuesta.status_code == 200
    assert len(respuesta.get_json()) == 3


def test_crear_persona(cliente):
    respuesta = cliente.post("/api/people", json={"lname": "Diaz", "fname": "Lucia"})
    assert respuesta.status_code == 201
    cuerpo = respuesta.get_json()
    assert cuerpo["lname"] == "Diaz"
    assert cuerpo["pizzas"] == []


def test_crear_persona_duplicada_da_406(cliente):
    respuesta = cliente.post("/api/people", json={"lname": "Gomez", "fname": "Otra"})
    assert respuesta.status_code == 406


def test_persona_inexistente_da_404(cliente):
    respuesta = cliente.get("/api/people/NoExiste")
    assert respuesta.status_code == 404


def test_crear_persona_con_apellido_vacio_da_400(cliente):
    respuesta = cliente.post("/api/people", json={"lname": "   ", "fname": "Test"})
    assert respuesta.status_code == 400


def test_actualizar_persona_da_200(cliente):
    respuesta = cliente.put(
        "/api/people/Gomez", json={"lname": "Gomez", "fname": "Cintya Maria"}
    )
    assert respuesta.status_code == 200
    assert respuesta.get_json()["fname"] == "Cintya Maria"


def test_borrar_persona_da_204(cliente):
    respuesta = cliente.delete("/api/people/Lopez")
    assert respuesta.status_code == 204
    assert respuesta.data == b""


def test_borrado_en_cascada(cliente):
    assert len(cliente.get("/api/pizzas").get_json()) == 3

    assert cliente.delete("/api/people/Sanchez").status_code == 204

    # Las dos pizzas de Sanchez se tienen que haber ido con Ã©l.
    assert len(cliente.get("/api/pizzas").get_json()) == 1
    assert cliente.get("/api/people/Sanchez").status_code == 404


# ---------------------------- Pizzas ----------------------------

def test_crear_pizza(cliente):
    persona = _id_de(cliente, "Gomez")
    respuesta = cliente.post(
        "/api/pizzas",
        json={
            "person_id": persona,
            "content": "Pizza Fugazzeta",
            "price": 8200.0,
            "size": "grande",
        },
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.get_json()
    assert cuerpo["content"] == "Pizza Fugazzeta"
    assert cuerpo["price"] == 8200.0
    assert cuerpo["size"] == "grande"


def test_crear_pizza_con_persona_inexistente_da_404(cliente):
    respuesta = cliente.post(
        "/api/pizzas",
        json={"person_id": 9999, "content": "Pizza Test", "price": 5000.0, "size": "chica"},
    )
    assert respuesta.status_code == 404


def test_crear_pizza_con_precio_negativo_da_400(cliente):
    persona = _id_de(cliente, "Gomez")
    respuesta = cliente.post(
        "/api/pizzas",
        json={"person_id": persona, "content": "Pizza Test", "price": -100.0, "size": "chica"},
    )
    assert respuesta.status_code == 400


def test_crear_pizza_con_precio_cero_da_400(cliente):
    persona = _id_de(cliente, "Gomez")
    respuesta = cliente.post(
        "/api/pizzas",
        json={"person_id": persona, "content": "Pizza Test", "price": 0, "size": "chica"},
    )
    assert respuesta.status_code == 400


def test_crear_pizza_con_tamano_invalido_da_400(cliente):
    persona = _id_de(cliente, "Gomez")
    respuesta = cliente.post(
        "/api/pizzas",
        json={"person_id": persona, "content": "Pizza Test", "price": 5000.0, "size": "familiar"},
    )
    assert respuesta.status_code == 400


def test_crear_pizza_con_descripcion_vacia_da_400(cliente):
    persona = _id_de(cliente, "Gomez")
    respuesta = cliente.post(
        "/api/pizzas",
        json={"person_id": persona, "content": "   ", "price": 5000.0, "size": "chica"},
    )
    assert respuesta.status_code == 400


def test_actualizar_pizza_da_200(cliente):
    pizza_id = cliente.get("/api/people/Gomez/pizzas").get_json()[0]["id"]
    respuesta = cliente.put(
        f"/api/pizzas/{pizza_id}",
        json={"content": "Pizza Napolitana", "price": 7500.0, "size": "mediana"},
    )
    assert respuesta.status_code == 200
    assert respuesta.get_json()["content"] == "Pizza Napolitana"


def test_pizza_inexistente_da_404(cliente):
    assert cliente.get("/api/pizzas/9999").status_code == 404


# ----------------------- Endpoints nuevos -----------------------

def test_listar_todas_las_pizzas(cliente):
    respuesta = cliente.get("/api/pizzas")
    assert respuesta.status_code == 200
    assert len(respuesta.get_json()) == 3


def test_filtrar_pizzas_por_persona(cliente):
    persona = _id_de(cliente, "Sanchez")
    respuesta = cliente.get(f"/api/pizzas?person_id={persona}")
    assert respuesta.status_code == 200
    assert len(respuesta.get_json()) == 2


def test_filtrar_pizzas_con_persona_inexistente_da_404(cliente):
    assert cliente.get("/api/pizzas?person_id=9999").status_code == 404


def test_pizzas_de_una_persona(cliente):
    respuesta = cliente.get("/api/people/Sanchez/pizzas")
    assert respuesta.status_code == 200
    assert len(respuesta.get_json()) == 2


def test_pizzas_de_persona_inexistente_da_404(cliente):
    assert cliente.get("/api/people/NoExiste/pizzas").status_code == 404


def test_resumen_de_una_persona(cliente):
    respuesta = cliente.get("/api/people/Sanchez/resumen")
    assert respuesta.status_code == 200
    cuerpo = respuesta.get_json()
    assert cuerpo["lname"] == "Sanchez"
    assert cuerpo["fname"] == "Ricardo"
    assert cuerpo["cantidad_pizzas"] == 2
    assert cuerpo["total_gastado"] == 15700.0


def test_resumen_de_persona_sin_pizzas(cliente):
    cuerpo = cliente.get("/api/people/Lopez/resumen").get_json()
    assert cuerpo["cantidad_pizzas"] == 0
    assert cuerpo["total_gastado"] == 0


def test_resumen_de_persona_inexistente_da_404(cliente):
    assert cliente.get("/api/people/NoExiste/resumen").status_code == 404