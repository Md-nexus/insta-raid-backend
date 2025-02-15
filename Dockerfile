# Use Node.js as base
FROM node:latest

# Install Python and required packages
RUN apt update && apt install -y python3 python3-pip python3-venv

# Create a virtual environment
RUN python3 -m venv /env

# Activate the virtual environment
ENV PATH="/env/bin:$PATH"

# Install yt-dlp
RUN pip install yt-dlp

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