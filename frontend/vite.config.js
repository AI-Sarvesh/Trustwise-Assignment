import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
  },
  server: {
    host: '0.0.0.0',  // Required for Docker
    port: 5173,
    watch: {
      usePolling: true  // Required for Docker on some systems
    }
  }
})
