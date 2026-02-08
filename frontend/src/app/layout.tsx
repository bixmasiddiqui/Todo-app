import type { Metadata } from 'next'
import { Press_Start_2P, Inter } from 'next/font/google'
import './globals.css'

const pressStart = Press_Start_2P({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-pixel',
})

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'Quest Log - Todo RPG',
  description: 'Level up your productivity! A gamified todo application.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${pressStart.variable} ${inter.variable} font-sans`}>{children}</body>
    </html>
  )
}
