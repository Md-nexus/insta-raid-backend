const express = require("express"); const cors = require("cors"); const {
    exec
} = require("child_process");

const app = express(); app.use(cors());

app.get("/extract", (req, res) => {
    const {
        url
    } = req.query;

    if (!url || !url.includes("instagram.com")) {
        return res.status(400).json({
            error: "Invalid Instagram URL"
        });
    }

    console.log(`Extracting video from: ${url}`);

    exec(`python3 extract.py "${url}"`, (error, stdout, stderr) => {
        if (error) {
            console.error("Error running Python script:", stderr);
            return res.status(500).json({
                error: "Server error. Try again later."
            });
        }

        console.log(`Extracted video URL: ${stdout.trim()}`);
        res.json({
            videoUrl: stdout.trim()
        });
    });

});

const PORT = process.env.PORT || 3000; app.listen(PORT, () => console.log(Server running on port $ {
    PORT
}));
