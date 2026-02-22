import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import NodeGlobalsPolyfillPlugin from '@esbuild-plugins/node-globals-polyfill';
import NodeModulesPolyfillPlugin from 'vite-plugin-node-polyfills';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    NodeModulesPolyfillPlugin()
  ],
  optimizeDeps: {
    esbuildOptions: {
      // Node.js global to browser globalThis
      define: {
        global: 'globalThis',
      },
      // Enable esbuild polyfill plugins
      plugins: [
        NodeGlobalsPolyfillPlugin({
          buffer: true,
          process: true,
        }),
      ],
    },
  },
  build: {
    rollupOptions: {
      // Ensure these modules are treated as external
      external: ['crypto'],
    },
  },
});
