FROM node:18-bullseye

RUN apt update && apt install -y python3 python3-pip python3-venv && \
    python3 -m venv /env && \
    /env/bin/pip install --upgrade yt-dlp playwright && \
    /env/bin/playwright install && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/env/bin:$PATH"
WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev

COPY . .

EXPOSE 3000
CMD ["node", "index.js"]
