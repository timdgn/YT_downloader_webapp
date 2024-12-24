import streamlit as st
import youtube_downloader

def main():
    st.title("YouTube Video Downloader 🎞️")

    # Create two tabs
    video_tab, playlist_tab = st.tabs(["Download Videos", "Download Playlist"])

    # Videos Tab
    with video_tab:
        
        st.markdown("#####")

        urls = st.text_area(
            "Enter YouTube URL(s)",
            help="For multiple videos, enter URLs separated by spaces. Each URL should be a complete YouTube link."
        )

        quality = st.selectbox(
            "Select video quality",
            ["low", "medium", "high", "very high"],
            format_func=lambda x: {
                "low": "Low (360p)",
                "medium": "Medium (720p)",
                "high": "High (1080p)",
                "very high": "Very High (4K)"
            }[x]
        )

        st.markdown("#####")

        if st.button("Download Videos 🔥"):
            if urls:
                with st.spinner("Downloading videos... Please wait"):
                    try:
                        # Split URLs by space and filter out empty strings
                        url_list = [url.strip() for url in urls.split() if url.strip()]
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        for i, url in enumerate(url_list):
                            filename = youtube_downloader.download_video(url, quality)
                            if filename:
                                st.success(f"Successfully downloaded: {filename}")
                            # Update progress
                            progress_bar.progress((i + 1) / len(url_list))
                        
                        st.success("All downloads completed!")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter at least one URL")

    # Playlist Tab
    with playlist_tab:

        st.markdown("#####")

        playlist_url = st.text_input(
            "Enter Playlist URL",
            help="Enter the URL of the YouTube playlist you want to download"
        )

        quality = st.selectbox(
            "Select video quality",
            ["low", "medium", "high", "very high"],
            format_func=lambda x: {
                "low": "Low (360p)",
                "medium": "Medium (720p)",
                "high": "High (1080p)",
                "very high": "Very High (4K)"
            }[x],
            key="playlist_quality"  # Unique key to avoid conflict with the other selectbox
        )

        st.markdown("#####")

        if st.button("Download Playlist 🔥"):
            if playlist_url:
                with st.spinner("Downloading playlist... Please wait"):
                    try:
                        youtube_downloader.download_playlist(playlist_url, quality)
                        st.success("Playlist download completed!")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a playlist URL")

if __name__ == "__main__":
    main()