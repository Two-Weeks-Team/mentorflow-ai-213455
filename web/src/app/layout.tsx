import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "MentorFlow AI",
  description: "Privacy\u2011first AI coaching that delivers instant, structured guidance\u2014no subscription, no guesswork.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
