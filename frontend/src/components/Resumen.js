import { pesos } from "@/lib/formato";

export default function Resumen({ resumen }) {
  const { cantidad_pizzas, total_gastado } = resumen;

  return (
    <div className="tarjeta">
      <h3>Resumen de consumo</h3>
      <p className="dato">
        {cantidad_pizzas} pizza{cantidad_pizzas === 1 ? "" : "s"} · total gastado{" "}
        <strong>{pesos.format(total_gastado)}</strong>
      </p>
    </div>
  );
}