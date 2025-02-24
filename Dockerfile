FROM node:18-bullseye

# Install system dependencies for Playwright + Python
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 \
    libpango-1.0-0 libcairo2 libgtk-3-0 libx11-xcb1 \
    # any other missing libs from the error message
    && rm -rf /var/lib/apt/lists/*

# Then install Playwright + browsers
RUN npm install -g playwright && npx playwright install --with-deps

# Or install via pip if you're using a Python approach:
# RUN /env/bin/pip install --upgrade playwright && /env/bin/playwright install

# Create your venv, install yt-dlp, etc.
RUN python3 -m venv /env && /env/bin/pip install --upgrade yt-dlp

WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev

COPY . .
EXPOSE 3000
CMD ["node", "index.js"]