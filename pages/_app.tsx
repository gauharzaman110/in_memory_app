// frontend/pages/_app.tsx
import React from 'react';
import type { AppProps } from 'next/app';
import '../styles/globals.css'; // Assuming you have a globals.css
import { AuthProvider } from '@/contexts/auth';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}

export default MyApp;
