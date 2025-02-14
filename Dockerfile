# Use Node.js as the base image
FROM node:latest

# Install Python and yt-dlp dependencies
RUN apt update && apt install -y python3 curl ffmpeg

# Install yt-dlp (direct binary download)
RUN curl -sS https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+x /usr/local/bin/yt-dlp

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy application files
COPY . .

# Expose the necessary port
EXPOSE 3000

# Start the Node.js server
CMD ["node", "index.js"]
