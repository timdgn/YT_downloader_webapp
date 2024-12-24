import yt_dlp
import os

# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_format_id(resolution):
    if resolution in ["low", "360", "360p"]:
        return "18"  # 360p mp4
    elif resolution in ["medium", "720", "720p", "hd"]:
        return "22"  # 720p mp4
    elif resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        return "137+140"  # 1080p mp4 + m4a
    elif resolution in ["very high", "2160", "2160p", "4K", "4k"]:
        return "313+140"  # 2160p webm + m4a
    else:
        return "18"  # Default to 360p

def download_video(url, resolution):
    # Create output directory if it doesn't exist
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    format_id = get_format_id(resolution)
    ydl_opts = {
        'format': format_id,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            return f"{info['title']}.{info['ext']}"
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
            return None

def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)

def download_playlist(url, resolution):
    # Create output directory if it doesn't exist
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'format': get_format_id(resolution),
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(url, download=True)
        except Exception as e:
            print(f"Error downloading playlist {url}: {str(e)}")

def input_links():
    print("Enter the links of the videos (end by entering 'STOP'):")

    links = []
    link = ""

    while link.lower() != "stop":
        link = input()
        links.append(link)

    links.pop()

    return links