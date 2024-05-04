// Use defineConfig from 'vitest/config' for test configurations
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/static/",
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ['./tests/test-setup.ts']
  },
  build: {
    outDir: "../static/",
  },
});
