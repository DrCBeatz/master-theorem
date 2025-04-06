// Use defineConfig from 'vitest/config' for test configurations
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./test-setup.ts"],

    coverage: {
      reporter: ["text", "lcov", "html"],

      include: ["src/**/*.{js,ts,jsx,tsx}"],
      exclude: [
        "node_modules/",
        "test/",
        "**/*.d.ts",
        "**/vite-env.d.ts",
        "src/main.tsx",
      ],

      reportsDirectory: "./coverage",
    },
  },
});
