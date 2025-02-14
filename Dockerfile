#Use Node.js as base
FROM node:latest

#Install Python
RUN apt update && apt install -y python3

#Install yt-dlp
RUN apt update && apt install -y yt-dlp

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
