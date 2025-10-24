import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { Analytics } from '@vercel/analytics/next'
import { Toaster } from '@/components/ui/toaster'
import ChatbotWidget from '@/components/ChatbotWidget'
import './globals.css'

export const metadata: Metadata = {
  title: 'Orange Sage',
  description: 'Advanced Penetration Testing Platform',
  icons: '/favicon.ico',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressContentEditableWarning>
      <head>
        <style>{`
html {
  font-family: ${GeistSans.style.fontFamily};
  --font-sans: ${GeistSans.variable};
  --font-mono: ${GeistMono.variable};
}
        `}</style>
      </head>
      <body suppressContentEditableWarning={true}>
        {children}
        <Toaster />
        <ChatbotWidget />
        <Analytics />
      </body>
    </html>
  )
}
