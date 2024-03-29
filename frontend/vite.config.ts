// Use defineConfig from 'vitest/config' for test configurations
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/static/",
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
  },
  build: {
    outDir: "../static/",
  },
});
