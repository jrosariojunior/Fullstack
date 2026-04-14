import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Matemática Insana",
  description: "Desmistificar a matemática, transformar o difícil em fácil",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
