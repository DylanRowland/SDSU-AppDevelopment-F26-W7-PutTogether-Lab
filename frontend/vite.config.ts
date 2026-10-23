// defineConfig provides type-safe Vite configuration.
import { defineConfig } from "vite";

// The React plugin lets Vite compile JSX and React Fast Refresh.
import react from "@vitejs/plugin-react";

// Export the configuration Vite reads when the frontend starts.
export default defineConfig({
  // Enable React support.
  plugins: [react()],
});
