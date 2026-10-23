# Use Node.js to install packages and run the Vite development server.
FROM node:22-alpine

# Put the frontend project inside /app in the image.
WORKDIR /app

# Copy package manifests first to improve Docker layer caching.
COPY package*.json ./

# Install React, Vite, TypeScript, and their type definitions.
RUN npm install

# Copy the React source and Vite configuration.
COPY . .

# Docker Compose supplies this value at image build time.
ARG VITE_API_BASE_URL

# Vite exposes VITE_ variables to the browser application.
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Document the Vite port inside the container.
EXPOSE 5173

# Start Vite and bind it to the container's network interface.
CMD ["npm", "run", "dev"]
