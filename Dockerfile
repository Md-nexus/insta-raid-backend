# Use Node.js as base
FROM node:latest

# Install Python and pip
RUN apt update && apt install -y python3 python3-pip

# Install yt-dlp
RUN python3 -m pip install yt-dlp

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