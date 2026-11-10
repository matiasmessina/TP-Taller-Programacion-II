"use client";

import { useState } from "react";

export default function FormularioPersona({ onCrear }) {
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function manejarEnvio(evento) {
    evento.preventDefault(); // sin esto el navegador recarga la página
    setEnviando(true);

    const ok = await onCrear({ fname, lname });

    setEnviando(false);
    if (ok) {
      setFname("");
      setLname("");
    }
  }

  return (
    <form className="formulario" onSubmit={manejarEnvio}>
      <h2>Nueva persona</h2>
      <div className="campos">
        <label>
          Nombre
          <input value={fname} onChange={(e) => setFname(e.target.value)} />
        </label>
        <label>
          Apellido
          <input
            value={lname}
            onChange={(e) => setLname(e.target.value)}
            required
          />
        </label>
        <button className="principal" type="submit" disabled={enviando}>
          {enviando ? "Guardando…" : "Agregar"}
        </button>
      </div>
    </form>
  );
}