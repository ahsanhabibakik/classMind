import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ClerkProvider } from "@clerk/nextjs";
import { HealthBadge } from "@/components/HealthBadge";
import { AuthButtons } from "@/components/AuthButtons";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ClassMind - AI-Powered Routine Management",
  description: "Manage your daily routines with AI assistance",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body
          className={`${geistSans.variable} ${geistMono.variable} antialiased`}
        >
          <div className="min-h-screen bg-gray-50">
            {/* Header with Health Badge */}
            <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/80 backdrop-blur-sm">
              <div className="container mx-auto flex items-center justify-between px-6 py-4">
                <div>
                  <h1 className="text-xl font-bold">ClassMind</h1>
                  <p className="text-xs text-gray-500">AI-Powered Routine Management</p>
                </div>
                <div className="flex items-center gap-4">
                  <HealthBadge />
                  <AuthButtons />
                </div>
              </div>
            </header>
            
            {/* Main Content */}
            <main>{children}</main>
          </div>
        </body>
      </html>
    </ClerkProvider>
  );
}
