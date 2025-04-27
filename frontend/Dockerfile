# frontend/Dockerfile

# Use an official Node.js runtime as the base image
FROM node:18-bullseye

ARG MDB_PRO_KEY
ENV MDB_PRO_KEY=${MDB_PRO_KEY}

RUN apt-get update && apt-get install -y \
  pkg-config \
  libcairo2-dev \
  libpango1.0-dev \
  libjpeg-dev \
  libgif-dev \
  librsvg2-dev \
  && rm -rf /var/lib/apt/lists/*

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy key management scripts and package.json and package-lock.json (if available)
COPY scripts ./scripts
COPY package*.json ./

# ----- inject key, install, scrub key -----
  RUN node ./scripts/addKey.cjs \
  && npm install --verbose \        
  && node ./scripts/removeKey.cjs
 # ------------------------------------------
 
# Copy the rest of the frontend application code
COPY . .

# Expose the port Vite uses (default is 5173)
EXPOSE 5173

# Set environment variable for Docker's file change notifications (optional but recommended)
ENV CHOKIDAR_USEPOLLING=true

# Command to run the Vite development server
CMD ["npm", "run", "dev", "--", "--host"]
