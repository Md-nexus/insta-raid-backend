# Use Node.js as base
FROM node:latest

# Install Python
RUN apt update && apt install -y python3

# Install pipx
RUN python3 -m pip install pipx

# Install yt-dlp using pipx
RUN pipx install yt-dlp

# Set working directory
WORKDIR /app

# Copy package.json & install dependencies
COPY package*.json ./
RUN npm install

# Copy application files
COPY . .

# Expose port
EXPOSE 3000

# Start the server
CMD ["node", "index.js"]