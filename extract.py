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