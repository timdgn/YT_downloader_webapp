# YouTube Video Downloader 🎞️

A streamlined web application built with Streamlit that allows you to download YouTube videos and playlists in various quality settings.

## Features ✨

- Download single or multiple YouTube videos
- Download entire YouTube playlists
- Select video quality (360p to 4K)
- User-friendly interface
- Progress tracking for downloads
- Support for multiple video formats

## Quality Options 🎥

- Low (360p)
- Medium (720p)
- High (1080p)
- Very High (4K)

## Installation 🚀

1. Clone this repository:
```bash
git clone https://github.com/timdgn/YT_downloader_webapp.git
```
```bash
cd YT_downloader_webapp
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage 💻

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Choose between downloading individual videos or playlists

4. For videos:
   - Enter one or more YouTube URLs (separated by spaces)
   - Select desired video quality
   - Click "Download Videos 🔥"

5. For playlists:
   - Enter the playlist URL
   - Select desired video quality
   - Click "Download Playlist 🔥"

## Notes 📝

- Downloaded videos will be saved in the `output` directory
- Internet connection is required for downloading videos
- Download speed depends on your internet connection and the selected video quality
