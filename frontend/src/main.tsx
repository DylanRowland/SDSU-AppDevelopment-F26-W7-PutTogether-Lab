// StrictMode helps identify common React development mistakes.
import { StrictMode } from "react";

// createRoot attaches React to the HTML element with id="root".
import { createRoot } from "react-dom/client";
import App from "./App";

// Render the App component into index.html's root element.
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
