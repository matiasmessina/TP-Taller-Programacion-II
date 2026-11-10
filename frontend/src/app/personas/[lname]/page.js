"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getPersona, getResumen, crearPizza, borrarPizza } from "@/lib/api";
import TarjetaPizza from "@/components/TarjetaPizza";
import FormularioPizza from "@/components/FormularioPizza";
import Resumen from "@/components/Resumen";
import Mensaje from "@/components/Mensaje";
import Cargando from "@/components/Cargando";

export default function DetallePersona() {
  const { lname } = useParams(); // el [lname] de la carpeta

  const [persona, setPersona] = useState(null);
  const [resumen, setResumen] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  async function cargar() {
    try {
      setError("");
      // Las dos peticiones van en paralelo en vez de una después de la otra.
      const [p, r] = await Promise.all([getPersona(lname), getResumen(lname)]);
      setPersona(p);
      setResumen(r);
    } catch (e) {
      setError(e.message);
    } finally {
      setCargando(false);
    }
  }

  useEffect(() => {
    cargar();
  }, [lname]); // si cambia el apellido de la URL, vuelve a pedir

  async function manejarCrearPizza(datos) {
    try {
      setError("");
      await crearPizza({ ...datos, person_id: persona.id });
      await cargar();
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    }
  }

  async function manejarBorrarPizza(id) {
    try {
      setError("");
      await borrarPizza(id);
      await cargar();
    } catch (e) {
      setError(e.message);
    }
  }

  if (cargando) return <Cargando texto="Cargando persona…" />;

  if (!persona) {
    return (
      <>
        <Mensaje>{error}</Mensaje>
        <Link className="enlace" href="/">
          ← Volver a clientes
        </Link>
      </>
    );
  }

  return (
    <>
      <p>
        <Link className="enlace" href="/">
          ← Volver a clientes
        </Link>
      </p>

      <h2>
        {persona.fname} {persona.lname}
      </h2>

      <Mensaje>{error}</Mensaje>
      {resumen && <Resumen resumen={resumen} />}

      <FormularioPizza onCrear={manejarCrearPizza} />

      <h3>Pizzas pedidas</h3>
      {persona.pizzas.length === 0 ? (
        <p className="dato">Todavía no pidió ninguna pizza.</p>
      ) : (
        persona.pizzas.map((pizza) => (
          <TarjetaPizza
            key={pizza.id}
            pizza={pizza}
            onBorrar={manejarBorrarPizza}
          />
        ))
      )}
    </>
  );
}