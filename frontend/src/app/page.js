"use client";

import { useEffect, useState } from "react";
import { getPersonas, crearPersona, borrarPersona } from "@/lib/api";
import TarjetaPersona from "@/components/TarjetaPersona";
import FormularioPersona from "@/components/FormularioPersona";
import Mensaje from "@/components/Mensaje";
import Cargando from "@/components/Cargando";

export default function Inicio() {
  const [personas, setPersonas] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  async function cargar() {
    try {
      setError("");
      setPersonas(await getPersonas());
    } catch (e) {
      setError(e.message);
    } finally {
      setCargando(false);
    }
  }

  useEffect(() => {
    cargar();
  }, []); // [] = se ejecuta una sola vez, al montar

  async function manejarCrear(datos) {
    try {
      setError("");
      await crearPersona(datos);
      await cargar();
      return true;
    } catch (e) {
      setError(e.message);
      return false;
    }
  }

  async function manejarBorrar(lname) {
    try {
      setError("");
      await borrarPersona(lname);
      await cargar();
    } catch (e) {
      setError(e.message);
    }
  }

  if (cargando) return <Cargando texto="Cargando personas…" />;

  return (
    <>
      <h2>Clientes</h2>
      <Mensaje>{error}</Mensaje>
      <FormularioPersona onCrear={manejarCrear} />

      {personas.length === 0 ? (
        <p className="dato">No hay personas cargadas.</p>
      ) : (
        personas.map((persona) => (
          <TarjetaPersona
            key={persona.lname}
            persona={persona}
            onBorrar={manejarBorrar}
          />
        ))
      )}
    </>
  );
}