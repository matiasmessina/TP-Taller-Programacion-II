const BASE = "http://localhost:8000/api";

// Única función que habla con la API. Centraliza la URL base, el Content-Type
// y la traducción de un error HTTP a una excepción de JavaScript.
async function pedir(ruta, opciones = {}) {
  const respuesta = await fetch(`${BASE}${ruta}`, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });

  if (!respuesta.ok) {
    let detalle = `Error ${respuesta.status}`;
    try {
      const cuerpo = await respuesta.json();
      detalle = cuerpo.detail || cuerpo.title || detalle;
    } catch {
      // Algunas respuestas de error no traen cuerpo JSON.
    }
    throw new Error(detalle);
  }

  if (respuesta.status === 204) return null; // DELETE no devuelve contenido
  return respuesta.json();
}

export const getPersonas = () => pedir("/people");
export const getPersona = (lname) => pedir(`/people/${lname}`);
export const getResumen = (lname) => pedir(`/people/${lname}/resumen`);
export const getPizzasDe = (lname) => pedir(`/people/${lname}/pizzas`);
export const getPizzas = (personId) =>
  pedir(personId ? `/pizzas?person_id=${personId}` : "/pizzas");

export const crearPersona = (datos) =>
  pedir("/people", { method: "POST", body: JSON.stringify(datos) });
export const borrarPersona = (lname) =>
  pedir(`/people/${lname}`, { method: "DELETE" });

export const crearPizza = (datos) =>
  pedir("/pizzas", { method: "POST", body: JSON.stringify(datos) });
export const borrarPizza = (id) =>
  pedir(`/pizzas/${id}`, { method: "DELETE" });