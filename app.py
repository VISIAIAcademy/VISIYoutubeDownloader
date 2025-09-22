import streamlit as st
import yt_dlp
import os

st.title("🎬 YouTube Downloader (No ffmpeg needed)")

url = st.text_input("Enter YouTube video URL:")

if st.button("Download"):
    if not url:
        st.error("Please enter a valid URL")
    else:
        with st.spinner("Downloading..."):
            try:
                output_dir = "downloads"
                os.makedirs(output_dir, exist_ok=True)

                # Progressive MP4 (video+audio in one file, no merging required)
                ydl_opts = {
                    "format": "mp4[ext=mp4][vcodec^=avc1][acodec^=mp4a]/best[ext=mp4]",
                    "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filepath = ydl.prepare_filename(info)

                st.success(f"Downloaded: {os.path.basename(filepath)}")

                with open(filepath, "rb") as f:
                    st.download_button(
                        label="⬇️ Download video file",
                        data=f,
                        file_name=os.path.basename(filepath),
                        mime="video/mp4"
                    )

            except Exception as e:
                st.error(f"Error: {e}")
