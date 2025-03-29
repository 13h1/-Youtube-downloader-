import os
import yt_dlp
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt

console = Console()

def show_header():
    console.print(
        Panel.fit(
            "[bright_white]🌟 YouTube Downloader 🌟[/bright_white]",
            subtitle="Made by 1ql",
            border_style="bright_white",
            padding=(1, 1)
        )
    )

def get_download_folder():
    download_path = Path.home() / "Downloads" / "Youtube"
    download_path.mkdir(parents=True, exist_ok=True)
    return download_path

def get_user_input():
    url = Prompt.ask("\n[bold]Enter YouTube URL[/bold]")
    
    console.print("\n[bold]Select format:[/bold]")
    console.print("1. MP3 (audio only)")
    console.print("2. MP4 (video with audio)")
    
    format_choice = Prompt.ask(
        "[bold]Choose format (1 or 2)[/bold]",
        choices=["1", "2"],
        default="2"
    )
    
    return url, format_choice

def download_content(url, format_choice, output_folder):
    ydl_opts = {
        'outtmpl': str(output_folder / '%(title)s.%(ext)s').replace(" ", "_"),
        'quiet': True,
        'progress_hooks': [progress_hook],
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
        console.print("\n[bold yellow]Downloading audio (MP3)...[/bold yellow]")
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })
        console.print("\n[bold yellow]Downloading video (MP4)...[/bold yellow]")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            transient=True,
        ) as progress:
            global download_task
            download_task = progress.add_task("[green]Downloading...", total=100)
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format_choice == '1':
                filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")

    return filename

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').replace('%', '')
        try:
            download_task.completed = float(percent)
        except:
            pass

def main():
    try:
        show_header()
        output_folder = get_download_folder()
        url, format_choice = get_user_input()
        
        filename = download_content(url, format_choice, output_folder)
        
        console.print(
            Panel.fit(
                f"[bold green]✓ Download complete![/bold green]\n[white]{filename}[/white]",
                border_style="green"
            )
        )
        
    except Exception as e:
        console.print(
            Panel.fit(
                f"[bold red]⚠ Error![/bold red]\n[white]{str(e)}[/white]",
                border_style="red"
            )
        )
    finally:
        if os.name == 'nt':
            os.system("pause")
        else:
            input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
