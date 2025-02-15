<<<<<<< HEAD
import subprocess  
import json  
  
def extract_instagram_video(url):  
    try:  
        result = subprocess.run(  
            ["yt-dlp", "-g", url],  
            capture_output=True,  
            text=True,  
            check=True  
        )  
        video_url = result.stdout.strip().splitlines()[0]  
        return json.dumps({"videoUrl": video_url})  
    except subprocess.CalledProcessError as e:  
        return json.dumps({"error": str(e)})  
  
if __name__ == "__main__":  
    import sys  
    if len(sys.argv) > 1:  
        url = sys.argv[1]  
        print(extract_instagram_video(url))  
    else:  
        print(json.dumps({"error": "No URL provided"}))
=======
import subprocess
import json

def extract_instagram_video(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", url],
            capture_output=True,
            text=True,
            check=True
        )
        video_urls = result.stdout.strip().splitlines()
        if not video_urls:
            return json.dumps({"error": "No video URL found. Video may be private or unavailable."})

        return json.dumps({"videoUrl": video_urls[0]})
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip()
        return json.dumps({"error": f"Extraction failed: {error_message}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected error: {str(e)}"})

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
        print(extract_instagram_video(url))
    else:
        print(json.dumps({"error": "No URL provided"}))
>>>>>>> 21418db (Updated backend)
