import streamlit as st
from pytube import YouTube
import os

def download_youtube_video(url: str, output_path: str = ".", filename: str = None):
    yt = YouTube(url)
    # Get metadata
    title = yt.title
    views = yt.views
    length = yt.length  # in seconds
    description = yt.description
    rating = yt.rating

    # Choose the highest resolution stream
    stream = yt.streams.get_highest_resolution()

    # Download
    out_file = stream.download(output_path=output_path, filename=filename)

    return {
        "title": title,
        "views": views,
        "length": length,
        "description": description,
        "rating": rating,
        "filepath": out_file
    }

def main():
    st.title("YouTube Video Downloader")

    url = st.text_input("Enter YouTube video URL:")
    if st.button("Fetch & Download"):
        if not url:
            st.error("Please enter a valid YouTube URL.")
        else:
            with st.spinner("Downloading..."):
                try:
                    info = download_youtube_video(url, output_path="downloads")
                    st.success("Download completed!")
                    st.write("**Title:**", info["title"])
                    st.write("**Views:**", info["views"])
                    st.write("**Duration (sec):**", info["length"])
                    st.write("**Rating:**", info["rating"])
                    st.write("**Saved at:**", info["filepath"])

                    # Let user download through Streamlit
                    # Note: Streamlit expects a file-like or open() object
                    with open(info["filepath"], "rb") as f:
                        video_bytes = f.read()
                    # Provide download button
                    st.download_button(
                        label="Download video file",
                        data=video_bytes,
                        file_name=os.path.basename(info["filepath"]),
                        mime="video/mp4"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
