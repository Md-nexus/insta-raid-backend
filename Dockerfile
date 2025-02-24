# Use a specific stable Node.js version
FROM node:18-bullseye

# Install Python, pip, and create a virtual environment, then install yt-dlp
RUN apt update && apt install -y python3 python3-pip python3-venv && \
    python3 -m venv /env && \
    /env/bin/pip install --upgrade yt-dlp && \
    rm -rf /var/lib/apt/lists/*

# Set environment variable for virtual environment
ENV PATH="/env/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy package.json & package-lock.json and install dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Copy the rest of the application files
COPY . .

# Expose port 3000
EXPOSE 3000

# Start the server
CMD ["node", "index.js"]