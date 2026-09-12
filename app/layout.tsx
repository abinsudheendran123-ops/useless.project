import type { Metadata } from "next";
import "../globals.css";

export const metadata: Metadata = {
  title: "Minecraft Battery HUD",
  description: "Monitor your laptop battery with Minecraft flair!",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-minecraft-dark min-h-screen flex items-center justify-center p-5">
        {children}
      </body>
    </html>
  );
}
