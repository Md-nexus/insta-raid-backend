# Use a specific stable Node.js version
FROM node:18-bullseye

# Install Python, pip, and yt-dlp in one command to reduce layers
RUN apt update && apt install -y python3 python3-pip python3-venv && \
    python3 -m venv /env && \
    /env/bin/pip install yt-dlp && \
    rm -rf /var/lib/apt/lists/*  # Clean up unused files to reduce image size

# Set environment variable for virtual environment
ENV PATH="/env/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy package.json & install dependencies
COPY package*.json ./
RUN npm install --omit=dev  # Install only production dependencies

# Copy application files
COPY . .

# Expose port
EXPOSE 3000

# Start the server
CMD ["node", "index.js"]