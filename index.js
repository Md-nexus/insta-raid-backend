const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");

const app = express();
app.use(cors());

app.get("/extract", (req, res) => {
    const { url } = req.query;
<<<<<<< HEAD

=======
>>>>>>> 21418db (Updated backend)
    if (!url || !url.includes("instagram.com")) {
        return res.status(400).json({ error: "Invalid Instagram URL" });
    }

    console.log(`Extracting video from: ${url}`);

    const pythonProcess = spawn("python3", ["extract.py", url]);

    let output = "";
<<<<<<< HEAD

=======
>>>>>>> 21418db (Updated backend)
    pythonProcess.stdout.on("data", (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
<<<<<<< HEAD
        console.error("Python Error:", data.toString());
    });

    pythonProcess.on("close", (code) => {
        try {
            const result = JSON.parse(output);
            res.json(result);
        } catch (err) {
            res.status(500).json({ error: "Failed to parse response from Python script." });
=======
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
            res.status(500).json({ error: "Failed to extract video URL." });
>>>>>>> 21418db (Updated backend)
        }
    });
});

const PORT = process.env.PORT || 3000;
<<<<<<< HEAD
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
=======
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
>>>>>>> 21418db (Updated backend)
