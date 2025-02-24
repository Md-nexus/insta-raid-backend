import subprocess
import json
import sys

def extract_instagram_metadata(url):
    try:
        # Run yt-dlp in JSON mode with a custom User-Agent header
        # Adjust the User-Agent string as needed.
        result = subprocess.run(
            [
                "yt-dlp",
                "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "-J",
                url
            ],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)

        # Extract direct video URL:
        video_url = data.get("url")
        if not video_url:
            # Fallback: choose the first available MP4 format URL
            for fmt in data.get("formats", []):
                if fmt.get("ext") == "mp4":
                    video_url = fmt.get("url")
                    break

        # Extract uploader (username)
        username = data.get("uploader", "Unknown")

        # Extract thumbnail; if not present, use a placeholder.
        thumbnail = data.get("thumbnail", "https://via.placeholder.com/150")

        # Determine video name: use title if available; otherwise, fallback on first five words of description.
        title = data.get("title")
        if not title or title.strip() == "":
            description = data.get("description", "")
            words = description.split()
            title = " ".join(words[:5]) if words else "Untitled"

        # Build a list of available MP4 formats
        available_formats = []
        for fmt in data.get("formats", []):
            if fmt.get("ext") == "mp4":
                quality = fmt.get("format_note", "Unknown")
                resolution = fmt.get("height", "Unknown")
                size = fmt.get("filesize") or fmt.get("filesize_approx") or 0
                available_formats.append({
                    "format_id": fmt.get("format_id"),
                    "quality": quality,
                    "resolution": resolution,
                    "size": size,
                    "url": fmt.get("url")
                })

        # Add placeholder conversion options for audio-only or no-sound video
        conversion_options = [
            {"option": "Audio Only", "format": "mp3", "note": "Convert video to audio-only."},
            {"option": "Video (No Sound)", "format": "mp4-ns", "note": "Convert video to a no-sound version."}
        ]

        result_data = {
            "videoUrl": video_url,
            "username": username,
            "thumbnail": thumbnail,
            "videoName": title,
            "availableFormats": available_formats,
            "conversionOptions": conversion_options
        }

        return json.dumps(result_data)
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else str(e)
        return json.dumps({"error": f"Extraction failed: {error_message}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
        print(extract_instagram_metadata(url))
    else:
        print(json.dumps({"error": "No URL provided"}))