const express = require("express");
const puppeteer = require("puppeteer-core");
const chromium = require("chrome-aws-lambda");
const cors = require("cors");

const app = express();
app.use(cors()); // Allow requests from any domain

// Extract Instagram Video URL
app.get("/extract", async (req, res) => {
    const { url } = req.query;
    
    if (!url || !url.includes("instagram.com")) {
        return res.status(400).json({ error: "Invalid Instagram URL" });
    }

    try {
        // Launch Puppeteer with AWS Lambda-compatible settings
        const browser = await puppeteer.launch({
            args: chromium.args,
            executablePath: await chromium.executablePath,
            headless: chromium.headless
        });

        const page = await browser.newPage();
        await page.goto(url, { waitUntil: "networkidle2" });

        // Extract the direct video URL
        const videoUrl = await page.evaluate(() => {
            const videoElement = document.querySelector("video");
            return videoElement ? videoElement.src : null;
        });

        await browser.close();

        if (!videoUrl) {
            return res.status(404).json({ error: "Could not extract video URL. Login may be required." });
        }

        return res.json({ videoUrl });

    } catch (error) {
        console.error("Error extracting video:", error);
        return res.status(500).json({ error: "Server error. Try again later." });
    }
});

// Ensure Railway uses the correct port
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));