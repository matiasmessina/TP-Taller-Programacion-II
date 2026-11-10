# TP Taller de Programación II — API REST de Personas y Pizzas

API REST en Python que administra los clientes de una pizzería y las pizzas que
pidió cada uno (relación 1 a N), más un frontend en React / Next.js que la
consume.

**Alumno:** Matías Messina
**Materia:** Taller de Programación II — Universidad FASTA

## Tecnologías

| Capa | Tecnología |
| --- | --- |
| Servidor web | Flask 2.3 |
| Contrato de la API | Connexion 2.x + OpenAPI 3.0 (`swagger.yml`) |
| Persistencia | SQLAlchemy 2.x + SQLite |
| Serialización | Marshmallow |
| Documentación y pruebas manuales | Swagger UI |
| Pruebas automáticas | pytest |
| Frontend | React 19 + Next.js (App Router) |

## Requisitos previos

- **Python 3.10 o superior** (probado con 3.14)
- **Node.js 18 o superior** — solo si querés levantar el frontend

## Instalar y levantar la API

Todos los comandos se ejecutan desde la raíz del proyecto.

**1. Crear el entorno virtual** (una sola vez):

```bash
python -m venv venv
```

**2. Activarlo** (cada vez que abras una terminal nueva):

```bash
venv\Scripts\Activate.ps1      # Windows (PowerShell)
source venv/bin/activate       # macOS / Linux
```

Si Windows rechaza el script con *"la ejecución de scripts está deshabilitada"*,
habilitalo una vez con
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.

**3. Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

**4. Crear la base de datos con los datos de ejemplo:**

```bash
python build_database.py
```

**5. Levantar el servidor:**

```bash
python app.py
```

La terminal muestra `Running on http://127.0.0.1:8000`. Dejala abierta: con
`Ctrl + C` se detiene el servidor.

| URL | Qué es |
| --- | --- |
| `http://localhost:8000/` | Página de inicio en HTML (plantilla Jinja2) |
| `http://localhost:8000/api/ui/` | Swagger UI: documentación interactiva y consola de pruebas |
| `http://localhost:8000/api/openapi.json` | El contrato OpenAPI en JSON |

> **Atención:** `build_database.py` ejecuta `db.drop_all()`, o sea que borra y
> recrea todas las tablas. Usalo para reiniciar los datos de ejemplo, no cuando
> tengas datos propios que quieras conservar.

## Correr las pruebas automáticas

Con el entorno virtual activado y **sin necesidad de tener el servidor
levantado**:

```bash
pytest -v
```

Tienen que pasar las **24 pruebas** de `tests/test_api.py`.

**Cómo funcionan.** Las pruebas usan el **cliente de pruebas de Flask**
(`app.test_client()`), que simula peticiones HTTP contra la aplicación sin
levantar un servidor real ni abrir un puerto. `tests/conftest.py` define la
fixture `cliente`, que antes de cada prueba recrea las tablas y carga tres
personas de ejemplo, y al terminar las borra: así cada prueba corre sobre datos
limpios y no depende del orden de ejecución.

Para que las pruebas **no toquen `people.db`**, `config.py` lee la ruta de la
base desde la variable de entorno `DATABASE_URI` y, si no está definida, usa
`people.db` como siempre. `conftest.py` la apunta a una base temporal antes de
importar la aplicación.

Las pruebas cubren los listados, el alta, la actualización y el borrado de
personas y pizzas, el borrado en cascada, los tres endpoints nuevos, y los
casos de error: apellido duplicado (406), recurso inexistente (404) y datos
inválidos (400). Tres de ellas —`test_actualizar_persona_da_200`,
`test_borrar_persona_da_204` y `test_actualizar_pizza_da_200`— fijan las
correcciones de códigos de estado para que una modificación futura no las
revierta sin que nadie se entere.

## Endpoints

Todos cuelgan del prefijo `/api`, definido en `servers` dentro de `swagger.yml`.

### Personas

| Método | Ruta | Qué hace | Éxito | Errores |
| --- | --- | --- | --- | --- |
| `GET` | `/api/people` | Lista todas las personas con sus pizzas | 200 | — |
| `POST` | `/api/people` | Crea una persona | 201 | 400, 406 |
| `GET` | `/api/people/{lname}` | Trae una persona por apellido | 200 | 404 |
| `PUT` | `/api/people/{lname}` | Actualiza el nombre de una persona | 200 | 400, 404 |
| `DELETE` | `/api/people/{lname}` | Borra la persona y todas sus pizzas | 204 | 404 |
| `GET` | `/api/people/{lname}/pizzas` | Lista solo las pizzas de esa persona | 200 | 404 |
| `GET` | `/api/people/{lname}/resumen` | Devuelve `lname`, `fname`, `cantidad_pizzas` y `total_gastado` | 200 | 404 |

### Pizzas

| Método | Ruta | Qué hace | Éxito | Errores |
| --- | --- | --- | --- | --- |
| `GET` | `/api/pizzas` | Lista todas las pizzas. Acepta `?person_id=` para filtrar | 200 | 404 |
| `POST` | `/api/pizzas` | Crea una pizza asociada a una persona | 201 | 400, 404 |
| `GET` | `/api/pizzas/{pizza_id}` | Trae una pizza por ID | 200 | 404 |
| `PUT` | `/api/pizzas/{pizza_id}` | Reemplaza `content`, `price` y `size` | 200 | 400, 404 |
| `DELETE` | `/api/pizzas/{pizza_id}` | Borra una pizza | 204 | 404 |

Los endpoints marcados como nuevos respecto del proyecto original son
`GET /api/pizzas`, `GET /api/people/{lname}/pizzas` y
`GET /api/people/{lname}/resumen`.

### Campos de una pizza

| Campo | Tipo | Validación |
| --- | --- | --- |
| `person_id` | entero | Obligatorio al crear; tiene que existir la persona |
| `content` | texto | Obligatorio, no vacío ni solo espacios |
| `price` | número | Obligatorio, **mayor que 0** (`minimum` + `exclusiveMinimum`) |
| `size` | texto | Obligatorio, solo `chica`, `mediana` o `grande` (`enum`) |

### Códigos de estado

| Código | Cuándo aparece |
| --- | --- |
| `200` | Lecturas y actualizaciones correctas |
| `201` | Creación de una persona o una pizza |
| `204` | Borrado de una persona o una pizza (sin cuerpo) |
| `400` | Falta un campo obligatorio, el precio no es mayor que 0, el tamaño no está en la lista, o un texto llegó vacío |
| `404` | La persona o la pizza no existe |
| `406` | Ya existe una persona con ese apellido |

## Levantar el frontend

El frontend es un proyecto Next.js independiente que consume la API por HTTP.
**Necesita que la API esté corriendo en el puerto 8000**, así que se trabaja con
dos terminales.

En una terminal nueva:

```bash
cd frontend
```

```bash
npm install
```

```bash
npm run dev
```

Después abrí `http://localhost:3000`.

| Ruta | Qué muestra |
| --- | --- |
| `/` | Lista de clientes, alta de persona y borrado |
| `/personas/{lname}` | Detalle de una persona, su resumen de consumo, alta y borrado de pizzas |
| `/pizzas` | Todas las pizzas, con filtro por persona |

Como el navegador bloquea las peticiones entre orígenes distintos
(`localhost:3000` → `localhost:8000`), la API habilita **CORS** solo para el
origen del frontend de desarrollo y solo bajo `/api/`, en `config.py`.

## Estructura del proyecto

```
TP_Messina_Matias/
├── app.py                 # punto de entrada: registra el contrato y la ruta /
├── config.py              # configuración central: Connexion, Flask, SQLAlchemy, Marshmallow, CORS
├── models.py              # modelos (Person, Pizza) y esquemas de Marshmallow
├── people.py              # lógica de personas: CRUD, pizzas y resumen
├── pizzas.py              # lógica de pizzas: CRUD y listado
├── build_database.py      # crea la base y carga los datos de ejemplo
├── swagger.yml            # contrato OpenAPI 3.0: la fuente de verdad de las rutas
├── requirements.txt       # dependencias de Python
├── README.md
├── templates/
│   └── home.html          # página de inicio (Jinja2)
├── tests/
│   ├── conftest.py        # base temporal y datos de ejemplo para las pruebas
│   └── test_api.py        # las 24 pruebas
├── informe/
│   ├── informe.pdf
│   └── capturas/
└── frontend/              # proyecto Next.js
    └── src/
        ├── app/           # rutas: cada carpeta es una URL
        ├── components/    # componentes reutilizables de React
        └── lib/           # cliente de la API y utilidades
```

En el App Router de Next.js, **cada carpeta dentro de `src/app/` es una ruta** y
el `page.js` que tiene adentro es la página. Por eso `src/app/pizzas/page.js` se
ve en `/pizzas`. `components/` y `lib/` van **al lado** de `app/`, no adentro,
justamente para que no se interpreten como rutas.

## Notas

- El proyecto está fijado a **Connexion 2.x** a propósito: Connexion 3 es ASGI y
  cambia las clases que usa `config.py`. Subir la versión obliga a reescribir
  `config.py` y `app.py`.
- Al correr `pytest` aparecen advertencias de deprecación de `jsonschema` y
  `asyncio` que provienen de Connexion 2 sobre Python 3.14, no del código del
  proyecto.
- `debug=True` en `app.py` es para el entorno de desarrollo. Fuera del aula tiene
  que estar en `False`, porque expone el depurador de Werkzeug.
