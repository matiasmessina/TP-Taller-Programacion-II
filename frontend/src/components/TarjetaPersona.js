import Link from "next/link";
import BotonBorrar from "./BotonBorrar";

export default function TarjetaPersona({ persona, onBorrar }) {
  const cantidad = persona.pizzas.length;

  return (
    <div className="tarjeta">
      <div className="fila">
        <div>
          <h3>
            <Link className="enlace" href={`/personas/${persona.lname}`}>
              {persona.fname} {persona.lname}
            </Link>
          </h3>
          <p className="dato">
            {cantidad === 0
              ? "Todavía no pidió ninguna pizza"
              : `${cantidad} pizza${cantidad > 1 ? "s" : ""} pedida${cantidad > 1 ? "s" : ""}`}
          </p>
        </div>
        <BotonBorrar onBorrar={() => onBorrar(persona.lname)} />
      </div>
    </div>
  );
}