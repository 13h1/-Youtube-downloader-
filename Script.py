import os
import yt_dlp
from pathlib import Path

def download_youtube_content():
    try:
        # Output folder (default: Downloads/Youtube)
        output_folder = os.path.join(os.path.expanduser("~"), "Downloads/Youtube")
        os.makedirs(output_folder, exist_ok=True)

        # URL input
        url = input("\nEnter YouTube URL: ").strip()

        # Format choice
        print("\nFormat:")
        print("1. MP3 (audio)")
        print("2. MP4 (video + audio)")
        format_choice = input("Choose (1 or 2): ").strip()

        # yt-dlp options
        ydl_opts = {
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'.replace(" ", "_")),  
            'quiet': False,
            'no_warnings': False,
        }

        if format_choice == '1':  
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
            print("\nDownloading audio (MP3)...")
        
        elif format_choice == '2':  
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            })
            print("\nDownloading video (MP4)...")
        
        else:
            print("Invalid choice. Exiting.")
            return

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if format_choice == '1':  
                filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")

        print(f"\nDownload complete: {filename}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    download_youtube_content()