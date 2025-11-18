import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'VineChat - Recomendação de Vinhos',
  description: 'Sistema de recomendação de vinhos usando LLM',
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

