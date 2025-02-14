const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
app.use(cors());

// Function to check if YT-DLP is installed
const checkYtDlp = async () => {
  return new Promise((resolve) => {
    exec("yt-dlp --version", (error) => {
      resolve(!error); // If no error, YT-DLP is installed
    });
  });
};

app.get("/extract", async (req, res) => {
  const { url } = req.query;

  if (!url || !url.includes("instagram.com")) {
    return res.status(400).json({ error: "Invalid Instagram URL" });
  }

  const isYtDlpInstalled = await checkYtDlp();
  if (!isYtDlpInstalled) {
    return res.status(500).json({ error: "YT-DLP is not installed on the server." });
  }

  try {
    console.log(`Extracting video from: ${url}`);

    const videoUrls = await new Promise((resolve, reject) => {
      exec(`yt-dlp -g ${url}`, { shell: "/bin/sh" }, (error, stdout, stderr) => {
        if (error) {
          reject(stderr || error.message);
        } else {
          resolve(stdout.trim().split("\n")); // Handles multiple formats
        }
      });
    });

    console.log(`Extracted video URLs:`, videoUrls);
    return res.json({ videoUrls });
  } catch (error) {
    console.error("Error extracting video:", error);
    return res.status(500).json({ error: "Failed to extract video URL. Try again later." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
