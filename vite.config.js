import { defineConfig } from 'vite'
// ensure Node has a web-crypto implementation (required by Vite internals)
// Node 16+ exposes webcrypto via `crypto.webcrypto`.
import { webcrypto } from 'crypto';
if (typeof globalThis.crypto === 'undefined') {
  // @ts-ignore
  globalThis.crypto = webcrypto;
}
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  base: '/',
})
