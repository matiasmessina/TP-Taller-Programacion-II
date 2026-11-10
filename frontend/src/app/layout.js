import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "Pizzería — Personas y Pizzas",
  description: "Front del TP de Taller de Programación II",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <header className="barra">
          <div className="contenedor">
            <h1>🍕 Pizzería</h1>
            <Link href="/">Personas</Link>
            <Link href="/pizzas">Pizzas</Link>
          </div>
        </header>

        <main className="contenedor">{children}</main>

        <footer className="pie">
          <div className="contenedor">
            TP Taller de Programación II — API REST de Personas y Pizzas
          </div>
        </footer>
      </body>
    </html>
  );
}