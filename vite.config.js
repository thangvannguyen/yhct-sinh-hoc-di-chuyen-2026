import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// base: './' keeps every asset path relative so the built site works both when
// served from a GitHub Pages project subpath (/yhct-sinh-hoc-di-chuyen-2026/)
// and locally.
export default defineConfig({
  base: './',
  plugins: [react(), tailwindcss()],
  // The question bank JSON is bundled and needed up front, so the single chunk
  // is expectedly large; raise the limit to keep build output clean.
  build: { chunkSizeWarningLimit: 900 },
})
