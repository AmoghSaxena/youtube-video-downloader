import streamlit as st
from pytube import YouTube, Playlist
import os
from pydub import AudioSegment
import validators

# Function to check if the URL is valid
def is_valid_url(url):
    return validators.url(url)

def download_audio(stream, output_path="audio"):
    # Download the audio stream
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    audio_stream = stream.download(output_path)
    # Convert the downloaded file to MP3 format
    audio = AudioSegment.from_file(audio_stream)
    filename = os.path.basename(audio_stream)
    audio.export(os.path.join(output_path, filename.replace('mp4', 'mp3')), format='mp3')
    return os.path.join(output_path, filename.replace('mp4', 'mp3'))

def download_video(stream, output_path="video"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return stream.download(output_path)

def main():
    st.title("YouTube Video Downloader")
    
    url = st.text_area("Paste your YouTube URL here", placeholder="https://www.youtube.com/watch?v=...")
    
    if not url:
        st.warning("Please paste a YouTube URL")
        return
    
    show_more_options = st.checkbox("Show more download options")
    
    try:
        # Use youtube.com or music.youtube.com URL
        yt = YouTube(url)
        
        # Show video title and duration
        st.header("Video Information")
        st.write(f"Title: {yt.title}")
        st.write(f"Author: {yt.author}")
        st.write(f"Length: {yt.length} seconds")
        st.write(f"Description: {yt.description[:200]}...")  # Show first 200 characters
        
        if show_more_options:
            # Get available resolutions and audio bitrates
            st.subheader("Available resolutions:")
            resolutions = [str(stream.resolution) for stream in yt.streams.fmt_streams if stream.resolution is not None]
            bitrates = [int(stream.bitrate) for stream in yt.streams if stream.bitrate is not None]
            bitrates = list(dict.fromkeys(bitrates))  # Remove duplicates
            
            # Resolution selection
            resolution = st.selectbox("Select resolution", resolutions)
            
            # Audio bitrate selection
            audio_bitrate = st.selectbox("Select audio bitrate (kb/s)", sorted(bitrates))
            
            # Only audio option
            audio_only = st.checkbox("Download only audio (convert to MP3)")
        else:
            # Default to highest quality
            resolution = max(resolutions, key=lambda x: int(x.split('x')[0]))
            audio_bitrate = max(bitrates)
            audio_only = st.checkbox("Download only audio (convert to MP3)", value=True)
        
        if audio_only:
            # Find audio-only stream
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4')
            if len(audio_stream) == 0:
                st.error("No audio-only stream available")
                return
            audio_stream = audio_stream.first()
            
            st.subheader("Audio Download")
            st.write("This will download the audio as an MP3 file")
            
            if st.button("Download Audio"):
                output_path = os.path.join(os.getcwd(), "audio")
                audio_file = download_audio(audio_stream, output_path)
                
                st.success("Download complete!")
                with open(audio_file, "rb") as file:
                    st.download_button(label="Download Audio",
                                      data=file,
                                      file_name=os.path.basename(audio_file))
        else:
            # Get the video stream with selected resolution and best audio
            if show_more_options:
                selected_resolution = resolution
                selected_bitrate = audio_bitrate
            else:
                selected_resolution = max(resolutions, key=lambda x: int(x.split('x')[0]))
                selected_bitrate = max(bitrates)
            
            st.subheader("Video Download")
            
            with st.expander("Advanced options"):
                st.write("Resolution:", selected_resolution)
                st.write("Bitrate:", selected_bitrate + " kb/s")
            
            if st.button("Download Video"):
                output_path = os.path.join(os.getcwd(), "video")
                video_file = download_video(yt.streams.filter(resolution=selected_resolution).first(), output_path)
                st.success("Download complete!")
                with open(video_file, "rb") as file:
                    st.download_button(label="Download Video",
                                      data=file,
                                      file_name=os.path.basename(video_file))
                
    except Exception as e:
        st.error("An error occurred during processing.")
        st.write(str(e))

if __name__ == "__main__":
    main()
    