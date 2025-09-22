import streamlit as st
import yt_dlp
import os

st.title("🎬 YouTube Downloader (Full Quality)")

url = st.text_input("Enter YouTube video URL:")

if st.button("Download"):
    if not url:
        st.error("Please enter a valid URL")
    else:
        with st.spinner("Downloading..."):
            try:
                output_dir = "downloads"
                os.makedirs(output_dir, exist_ok=True)

                # Best video + audio merged into MP4
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",
                    "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filepath = ydl.prepare_filename(info)

                # Ensure .mp4 extension after merging
                if not filepath.endswith(".mp4"):
                    filepath = filepath.rsplit(".", 1)[0] + ".mp4"

                st.success(f"Downloaded: {os.path.basename(filepath)}")

                # Provide download inside Streamlit
                with open(filepath, "rb") as f:
                    st.download_button(
                        label="⬇️ Download video file",
                        data=f,
                        file_name=os.path.basename(filepath),
                        mime="video/mp4"
                    )

            except Exception as e:
                st.error(f"Error: {e}")
