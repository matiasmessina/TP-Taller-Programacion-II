import { pesos } from "@/lib/formato";
import BotonBorrar from "./BotonBorrar";

export default function TarjetaPizza({ pizza, duenio, onBorrar }) {
  return (
    <div className="tarjeta">
      <div className="fila">
        <div>
          <h3>{pizza.content}</h3>
          <p className="dato">
            {pizza.size} · {pesos.format(pizza.price)}
            {duenio && ` · ${duenio}`}
          </p>
        </div>
        {onBorrar && <BotonBorrar onBorrar={() => onBorrar(pizza.id)} />}
      </div>
    </div>
  );
}