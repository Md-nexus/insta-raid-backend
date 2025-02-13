const express = require("express");
const puppeteer = require("puppeteer");
const cors = require("cors");

const app = express();
app.use(cors()); // Allow requests from any domain

app.get("/extract", async (req, res) => {
    const { url } = req.query;

    if (!url || !url.includes("instagram.com")) {
        return res.status(400).json({ error: "Invalid Instagram URL" });
    }

    try {
        console.log("Launching Puppeteer...");
        const browser = await puppeteer.launch({
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--mute-audio",
                "--no-zygote",
                "--single-process"
            ],
            headless: true // Run in headless mode
        });

        console.log("Puppeteer launched!");
        const page = await browser.newPage();
        console.log(`Navigating to: ${url}`);
        await page.goto(url, { waitUntil: "networkidle2" });

        // Extract the direct video URL
        console.log("Extracting video URL...");
        const videoUrl = await page.evaluate(() => {
            const videoElement = document.querySelector("video");
            return videoElement ? videoElement.src : null;
        });

        await browser.close();
        console.log("Browser closed.");

        if (!videoUrl) {
            console.log("No video URL found. Possible login requirement.");
            return res.status(404).json({ error: "Could not extract video URL. Login may be required." });
        }

        console.log(`Extracted video URL: ${videoUrl}`);
        return res.json({ videoUrl });

    } catch (error) {
        console.error("Error extracting video:", error);
        return res.status(500).json({ error: "Server error. Try again later." });
    }
});

// Use Railway's assigned port
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));