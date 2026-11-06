import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'
import { fileURLToPath, URL } from 'node:url'

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'icons.svg'],
      manifest: {
        name: 'SchemeNavigator — Indian Government Schemes',
        short_name: 'SchemeNavigator',
        description: 'Discover government schemes you may be eligible for with step-by-step application guidance.',
        theme_color: '#0F766E',
        background_color: '#F8FAFC',
        display: 'standalone',
        orientation: 'portrait-primary',
        scope: './',
        start_url: './',
        icons: [
          {
            src: 'favicon.svg',
            sizes: 'any',
            type: 'image/svg+xml',
            purpose: 'any maskable',
          },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,ico,woff2}'],
        runtimeCaching: [
          {
            urlPattern: ({ url }) => url.pathname.includes('/data/schemes'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'schemes-json-cache',
              expiration: {
                maxEntries: 10,
                maxAgeSeconds: 60 * 60 * 24 * 7, // 7 days
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern: /^https:\/\/fonts\.(googleapis|gstatic)\.com\/.*/i,
            handler: 'CacheFirst',
            options: {
              cacheName: 'google-fonts-cache',
              expiration: {
                maxEntries: 20,
                maxAgeSeconds: 60 * 60 * 24 * 365, // 1 year
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
        ],
      },
    }),
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




