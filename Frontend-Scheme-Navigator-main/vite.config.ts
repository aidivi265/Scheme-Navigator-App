import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/brabble-api': {
        target: 'https://brabble.ai',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/brabble-api/, ''),
      },
      '/parse-api': {
        target: 'https://api.parse.bot',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/parse-api/, ''),
      },
      '/mygov-rss': {
        target: 'https://www.mygov.in',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/mygov-rss/, ''),
      },
    },
  },
  preview: {
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/brabble-api': {
        target: 'https://brabble.ai',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/brabble-api/, ''),
      },
      '/parse-api': {
        target: 'https://api.parse.bot',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/parse-api/, ''),
      },
      '/mygov-rss': {
        target: 'https://www.mygov.in',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/mygov-rss/, ''),
      },
    },
  },
  build: {
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('src/i18n/locales/')) {
            const match = id.match(/locales[/\\]([^.]+)\.ts/);
            return match ? `locale-${match[1]}` : 'locales';
          }
          if (id.includes('src/i18n/glossary') || id.includes('src/i18n/schemeGlossary')) {
            return 'i18n-glossary';
          }
          if (id.includes('node_modules/framer-motion')) {
            return 'vendor-framer-motion';
          }
          if (id.includes('node_modules/lucide-react')) {
            return 'vendor-lucide';
          }
          if (
            id.includes('node_modules/react/') ||
            id.includes('node_modules/react-dom/') ||
            id.includes('node_modules/react-router-dom/')
          ) {
            return 'vendor-react-core';
          }
        },
      },
    },
  },
})




