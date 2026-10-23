// This Worker is a later deployment placeholder, not part of local Docker.
export default {
  // Cloudflare calls fetch when the Worker receives an HTTP request.
  async fetch(): Promise<Response> {
    // Return JSON so the placeholder can be tested independently.
    return Response.json({
      // This makes the missing Hyperdrive connection visible to students.
      message: "Cloudflare placeholder. Hyperdrive is not connected in the local lab.",
    });
  },
};
