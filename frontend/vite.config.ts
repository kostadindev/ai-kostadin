import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    allowedHosts: [
      'localhost',
      '5ed1-2600-4808-5931-a900-a48a-5409-62bc-5c0b.ngrok-free.app'
    ]
  }
})
