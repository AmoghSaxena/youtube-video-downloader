import streamlit as st
from pytube import YouTube
from io import BytesIO
import re
from typing import Union

# Configure page settings
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎬",
    layout="centered"
)

def validate_youtube_url(url: str) -> bool:
    """Validate YouTube and YouTube Music URLs"""
    pattern = (
        r'(https?://)?(www\.)?'
        '(youtube|music\.youtube)\.com/'
        '(watch\?v=|shorts/|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(pattern, url) is not None

def get_streams(url: str, media_type: str) -> Union[list, None]:
    """Retrieve available streams for the video"""
    try:
        yt = YouTube(url)
        if media_type == "video":
            return yt.streams.filter(
                progressive=True,
                file_extension='mp4',
                type='video'
            ).order_by('resolution').desc()
        return yt.streams.filter(
            only_audio=True
        ).order_by('abr').desc()
    except Exception as e:
        st.error(f"Error retrieving streams: {str(e)}")
        return None

def download_stream(stream) -> BytesIO:
    """Download stream to in-memory buffer"""
    buffer = BytesIO()
    stream.stream_to_buffer(buffer)
    buffer.seek(0)
    return buffer

# UI Components
st.title("🎥 YouTube Media Downloader")
st.markdown("""
    Download videos or audio from YouTube and YouTube Music  
    *Supports resolutions up to 720p without FFmpeg*
""")

url = st.text_input("Enter YouTube URL:", placeholder="https://youtube.com/watch?v=...")

if url:
    if not validate_youtube_url(url):
        st.error("Invalid YouTube URL. Please use either youtube.com or music.youtube.com links.")
        st.stop()
    
    media_type = st.radio(
        "Select download type:",
        ("Video", "Audio"),
        horizontal=True,
        index=0
    )
    
    streams = get_streams(url, media_type.lower())
    if not streams:
        st.error("No available streams found for this content")
        st.stop()
    
    if media_type == "Video":
        selected = st.selectbox(
            "Select resolution:",
            streams,
            format_func=lambda s: f"{s.resolution} ({s.fps}fps)"
        )
    else:
        selected = st.selectbox(
            "Select audio quality:",
            streams,
            format_func=lambda s: f"{s.abr} ({(s.filesize_mb):.1f} MB)"
        )
    
    if st.button("Prepare Download"):
        with st.spinner(f"Processing {media_type}..."):
            try:
                buffer = download_stream(selected)
                mime_type = "video/mp4" if media_type == "Video" else "audio/webm"
                
                st.success("Ready for download!")
                st.download_button(
                    label=f"Download {media_type}",
                    data=buffer,
                    file_name=selected.default_filename,
                    mime=mime_type,
                    help="File will be saved in your browser's default download location"
                )
            except Exception as e:
                st.error(f"Download failed: {str(e)}")

# Add footer with usage tips
st.markdown("---")
st.markdown("""
    **Usage Tips:**
    - For HD videos: Choose 720p resolution (if available)
    - For audio-only: Select highest ABR value for best quality
    - Shorts/embedded videos are supported
    - Downloads may take longer for larger files
""")
