FROM node:18-bullseye

# Install system dependencies for Playwright and Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    libpango-1.0-0 libcairo2 libgtk-3-0 libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Remove Node global Playwright install; we use the Python version instead
# RUN npm install -g playwright && npx playwright install --with-deps

# Create a Python virtual environment and install yt-dlp and Python Playwright
RUN python3 -m venv /env && \
    /env/bin/pip install --upgrade pip setuptools wheel && \
    /env/bin/pip install --upgrade yt-dlp playwright && \
    /env/bin/playwright install --with-deps chromium

WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
