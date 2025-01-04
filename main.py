import streamlit as st
from glob import glob
from youtube_downloader import *

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

        if st.button("Process video(s) 🔥"):
            if urls:
                with st.spinner("Downloading videos... Please wait"):
                    try:
                        # Split URLs by space and filter out empty strings
                        url_list = [url.strip() for url in urls.split() if url.strip()]
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        for i, url in enumerate(url_list):
                            filename = download_video(url, quality, OUTPUT_DIR)
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
            key="playlist_quality"
        )

        st.markdown("#####")

        if st.button("Process playlist 🔥"):
            if playlist_url:
                with st.spinner("Downloading playlist... Please wait"):
                    try:
                        download_playlist(playlist_url, quality)
                        st.success("Playlist download completed !")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a playlist URL")

    st.markdown("#####")

    # Add a section to display downloaded files
    st.subheader("Downloaded Files")
    # if OUTPUT_DIR does not exist
    if os.path.exists(OUTPUT_DIR):
        files = glob(os.path.join(OUTPUT_DIR, "*"))
        if files:
            for file in files:
                filename = os.path.basename(file)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(filename)
                with col2:
                    with open(file, "rb") as f:
                        if st.download_button(
                            label="Download",
                            data=f,
                            file_name=filename,
                            key=f"download_{filename}"):
                                # Delete the file after successful download
                                f.close()  # Close the file handle before deleting
                                os.remove(file)
                                st.rerun()  # Refresh the page to update the file list
        else:
            st.info("No files available for download")

if __name__ == "__main__":
    main()