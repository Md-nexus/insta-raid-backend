const express = require("express");
const cors = require("cors");
const { spawn, spawnSync } = require("child_process");

const app = express();
app.use(cors());
app.use(express.json()); // Parse JSON bodies for POST requests

// GET /extract?url=<url>
// Extract metadata for a single Instagram URL.
app.get("/extract", (req, res) => {
    const { url } = req.query;
    if (!url || !url.includes("instagram.com")) {
        return res.status(400).json({ error: "Invalid Instagram URL" });
    }

    console.log(`Extracting metadata from: ${url}`);

    const pythonProcess = spawn("python3", ["extract.py", url]);

    let output = "";
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error("Error running Python script:", data.toString());
    });

    pythonProcess.on("close", (code) => {
        if (code === 0) {
            try {
                res.json(JSON.parse(output));
            } catch (err) {
                res.status(500).json({ error: "Invalid JSON response from backend." });
            }
        } else {
            res.status(500).json({ error: "Failed to extract video metadata." });
        }
    });
});

// POST /extract-batch
// Accepts a JSON body with an array of Instagram URLs and returns metadata for each.
app.post("/extract-batch", (req, res) => {
    const { urls } = req.body;
    if (!urls || !Array.isArray(urls)) {
        return res.status(400).json({ error: "Invalid request: 'urls' must be an array." });
    }

    // Filter for valid Instagram URLs
    const instagramUrls = urls.filter(u => u && u.includes("instagram.com"));
    if (instagramUrls.length === 0) {
        return res.status(400).json({ error: "No valid Instagram URLs provided." });
    }

    let results = [];
    for (let url of instagramUrls) {
        // Process each URL synchronously
        const pythonProcess = spawnSync("python3", ["extract.py", url], { encoding: "utf-8" });
        if (pythonProcess.error) {
            results.push({ url, error: pythonProcess.error.message });
        } else {
            try {
                const jsonResponse = JSON.parse(pythonProcess.stdout);
                results.push({ url, data: jsonResponse });
            } catch (e) {
                results.push({ url, error: "Invalid JSON response." });
            }
        }
    }
    res.json({ results });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));