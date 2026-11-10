export default function BotonBorrar({ onBorrar, children = "Borrar" }) {
  return (
    <button className="borrar" onClick={onBorrar}>
      {children}
    </button>
  );
}