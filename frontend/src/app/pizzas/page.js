"use client";

import { useEffect, useState } from "react";
import { getPizzas, getPersonas } from "@/lib/api";
import TarjetaPizza from "@/components/TarjetaPizza";
import Mensaje from "@/components/Mensaje";
import Cargando from "@/components/Cargando";

export default function Pizzas() {
  const [pizzas, setPizzas] = useState([]);
  const [personas, setPersonas] = useState([]);
  const [filtro, setFiltro] = useState("");
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  // Las personas se piden una sola vez: sirven para el desplegable del filtro
  // y para mostrar de quién es cada pizza.
  useEffect(() => {
    getPersonas()
      .then(setPersonas)
      .catch((e) => setError(e.message));
  }, []);

  // Las pizzas se vuelven a pedir cada vez que cambia el filtro.
  useEffect(() => {
    let vigente = true;

    async function cargar() {
      try {
        setError("");
        setCargando(true);
        const datos = await getPizzas(filtro || undefined);
        if (vigente) setPizzas(datos);
      } catch (e) {
        if (vigente) setError(e.message);
      } finally {
        if (vigente) setCargando(false);
      }
    }

    cargar();

    // Función de limpieza: si el filtro cambia antes de que llegue la
    // respuesta anterior, se descarta en vez de pisar la lista nueva.
    return () => {
      vigente = false;
    };
  }, [filtro]);

  const nombrePorId = Object.fromEntries(
    personas.map((p) => [p.id, `${p.fname} ${p.lname}`])
  );

  return (
    <>
      <h2>Todas las pizzas</h2>
      <Mensaje>{error}</Mensaje>

      <div className="formulario">
        <div className="campos">
          <label>
            Filtrar por persona
            <select value={filtro} onChange={(e) => setFiltro(e.target.value)}>
              <option value="">Todas</option>
              {personas.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.fname} {p.lname}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      {cargando ? (
        <Cargando texto="Cargando pizzas…" />
      ) : pizzas.length === 0 ? (
        <p className="dato">No hay pizzas para mostrar.</p>
      ) : (
        pizzas.map((pizza) => (
          <TarjetaPizza
            key={pizza.id}
            pizza={pizza}
            duenio={nombrePorId[pizza.person_id]}
          />
        ))
      )}
    </>
  );
}