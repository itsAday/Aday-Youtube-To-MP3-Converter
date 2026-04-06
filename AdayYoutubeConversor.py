import sys
import os
import subprocess
import time

def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing libraries: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install_if_missing("yt_dlp")

import yt_dlp

def download_youtube_mp3(url, output_path='.'):
   
    success = True

    out_dir = os.path.join(output_path, 'mp3-downloads')
    os.makedirs(out_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{out_dir}/%(title)s.%(ext)s',
        'ffmpeg_location': r'ffmpeg\bin',
        'quiet': True,
        'no_warnings': True,
        'postprocessor_args': ['-loglevel', 'quiet'],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    
    null = open(os.devnull, 'w')
    try:
        original_stdout = sys.stdout
        original_stderr = sys.stderr


        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as error:
        success = False
        if "HTTP Error 403" in str(error):
            os.system('cls')
            print("Libraries outdated - Updating Now")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt_dlp"])
            os.system('cls')
            print("Update done, please restart script to validate changes.")
            time.sleep(5)
            sys.exit()
    finally:
        
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        null.close()

    
    return success


if __name__ == "__main__":
    while True:
        url = input("YouTube URL: ").strip()
        if not url:
            break

        try:
            success = download_youtube_mp3(url)
            if success:
                print("✅ Download complete")
            else:
                print("❌ Link not valid")
        except Exception as e:
            print("Error", e)
            
               
