#Use Node.js as base
FROM node:latest

#Install yt-dlp
RUN curl -sS https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

#Set working directory
WORKDIR /app

#Copy package.json & install dependencies
COPY package*.json ./
RUN npm install

#Copy application files
COPY . .

#Expose port
EXPOSE 3000

#Start the server
CMD ["node", "index.js"]
