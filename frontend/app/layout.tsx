import type { Metadata } from 'next'
import './globals.css'
export const metadata:Metadata={title:'Meeting Intelligence — Decision & Action Command Center',description:'Zero-key meeting-to-workflow automation for decisions, actions, risks, questions, status, and follow-up.'}
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
