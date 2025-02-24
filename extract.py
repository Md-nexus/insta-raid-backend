import subprocess
import json
import sys
from playwright.sync_api import sync_playwright

def extract_instagram_metadata(url):
    # First, try full metadata extraction with yt-dlp using JSON output
    metadata = try_full_metadata(url)
    if "error" not in metadata:
        return json.dumps(metadata)
    # If full metadata extraction fails, fallback to Playwright extraction
    fallback = try_playwright_extraction(url)
    return json.dumps(fallback)

def try_full_metadata(url):
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "-J",
                url
            ],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        # Extract direct video URL
        video_url = data.get("url")
        if not video_url:
            for fmt in data.get("formats", []):
                if fmt.get("ext") == "mp4":
                    video_url = fmt.get("url")
                    break
        if not video_url:
            return {"error": "No video URL found; possibly restricted."}
        # Extract uploader/username
        username = data.get("uploader", "Unknown")
        # Extract thumbnail
        thumbnail = data.get("thumbnail", "https://via.placeholder.com/150")
        # Determine video name: use title if present; otherwise, fallback to first five words of description
        title = data.get("title", "").strip()
        if not title:
            description = data.get("description", "")
            words = description.split()
            title = " ".join(words[:5]) if words else "Untitled"
        # Build list of available MP4 formats
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
        # Placeholder conversion options
        conversion_options = [
            {"option": "Audio Only", "format": "mp3", "note": "Convert video to audio-only."},
            {"option": "Video (No Sound)", "format": "mp4-ns", "note": "Convert video to a no-sound version."}
        ]
        return {
            "videoUrl": video_url,
            "username": username,
            "thumbnail": thumbnail,
            "videoName": title,
            "availableFormats": available_formats,
            "conversionOptions": conversion_options
        }
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.strip() if e.stderr else str(e)
        return {"error": f"Full metadata extraction failed: {err_msg}"}
    except Exception as e:
        return {"error": f"Unexpected error in full metadata extraction: {str(e)}"}

def try_playwright_extraction(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle", timeout=60000)
            
            # Extract metadata using meta tags
            title = page.get_attribute('meta[property="og:title"]', "content") or ""
            thumbnail = page.get_attribute('meta[property="og:image"]', "content") or "https://via.placeholder.com/150"
            video_url = page.get_attribute('meta[property="og:video"]', "content")
            # Fallback for title: try description
            if not title:
                description = page.get_attribute('meta[property="og:description"]', "content") or ""
                words = description.split()
                title = " ".join(words[:5]) if words else "Untitled"
            
            # Attempt to extract author info from JSON-LD (if available)
            ld_elem = page.query_selector('script[type="application/ld+json"]')
            if ld_elem:
                try:
                    ld_data = json.loads(ld_elem.inner_text())
                    username = ld_data.get("author", {}).get("name", "Unknown")
                except Exception:
                    username = "Unknown"
            else:
                username = "Unknown"
            
            browser.close()

            # Return the metadata with empty availableFormats (since we don't have them here)
            conversion_options = [
                {"option": "Audio Only", "format": "mp3", "note": "Convert video to audio-only."},
                {"option": "Video (No Sound)", "format": "mp4-ns", "note": "Convert video to a no-sound version."}
            ]
            return {
                "videoUrl": video_url if video_url else "",
                "username": username,
                "thumbnail": thumbnail,
                "videoName": title,
                "availableFormats": [],
                "conversionOptions": conversion_options
            }
    except Exception as e:
        return {"error": f"Playwright extraction failed: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
        print(extract_instagram_metadata(url))
    else:
        print(json.dumps({"error": "No URL provided"}))
