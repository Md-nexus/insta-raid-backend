import subprocess
import json
import sys

def extract_instagram_metadata(url):
    try:
        # Run yt-dlp in JSON mode to get full metadata
        result = subprocess.run(
            ["yt-dlp", "-J", url],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)

        # Extract direct video URL:
        video_url = data.get("url")
        if not video_url:
            # If not directly provided, try to pick the first MP4 format from the "formats" list
            for fmt in data.get("formats", []):
                if fmt.get("ext") == "mp4":
                    video_url = fmt.get("url")
                    break

        # Extract uploader/username:
        username = data.get("uploader", "Unknown")

        # Extract thumbnail:
        thumbnail = data.get("thumbnail", "https://via.placeholder.com/150")

        # Determine video name:
        title = data.get("title")
        if not title or title.strip() == "":
            description = data.get("description", "")
            words = description.split()
            title = " ".join(words[:5]) if words else "Untitled"

        # Build a list of available MP4 formats:
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

        # Add placeholder conversion options (to be implemented later with FFmpeg)
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