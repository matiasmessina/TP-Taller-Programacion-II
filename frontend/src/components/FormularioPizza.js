"use client";

import { useState } from "react";

// Los mismos tres valores del enum de swagger.yml.
const TAMANOS = ["chica", "mediana", "grande"];

export default function FormularioPizza({ onCrear }) {
  const [content, setContent] = useState("");
  const [price, setPrice] = useState("");
  const [size, setSize] = useState("mediana");
  const [enviando, setEnviando] = useState(false);

  async function manejarEnvio(evento) {
    evento.preventDefault();
    setEnviando(true);

    // price se convierte a número: el input siempre devuelve texto, y la API
    // espera un number. Sin el Number() la validación del contrato da 400.
    const ok = await onCrear({ content, price: Number(price), size });

    setEnviando(false);
    if (ok) {
      setContent("");
      setPrice("");
      setSize("mediana");
    }
  }

  return (
    <form className="formulario" onSubmit={manejarEnvio}>
      <h2>Agregar pizza</h2>
      <div className="campos">
        <label>
          Descripción
          <input
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </label>
        <label>
          Precio
          <input
            type="number"
            min="1"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </label>
        <label>
          Tamaño
          <select value={size} onChange={(e) => setSize(e.target.value)}>
            {TAMANOS.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </label>
        <button className="principal" type="submit" disabled={enviando}>
          {enviando ? "Guardando…" : "Agregar"}
        </button>
      </div>
    </form>
  );
}