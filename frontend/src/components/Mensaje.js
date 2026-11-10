export default function Mensaje({ tipo = "error", children }) {
  if (!children) return null; // si no hay mensaje, no renderiza nada
  return <div className={`mensaje ${tipo}`}>{children}</div>;
}