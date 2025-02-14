FROM node:latest

Install yt-dlp
RUN curl -sL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod +x /usr/local/bin/yt-dlp

Set working directory to /app
WORKDIR /app

Copy package*.json
COPY package*.json ./

Install dependencies
RUN npm install

Copy application code
COPY . .

Expose port
EXPOSE 3000

Run command
CMD ["node", "index.js"]
