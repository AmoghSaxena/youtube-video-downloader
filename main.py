import streamlit as st
from pytube import YouTube
import validators

def is_valid_url(url):
    return validators.url(url)

def download_audio(stream, output_path="audio"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return stream.download(output_path)

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
        yt = YouTube(url)
        
        st.header("Video Information")
        st.write(f"Title: {yt.title}")
        st.write(f"Author: {yt.author}")
        st.write(f"Length: {yt.length} seconds")
        st.write(f"Description: {yt.description[:200]}...")

        if show_more_options:
            resolutions = [str(stream.resolution) for stream in yt.streams if stream.resolution is not None]
            audio_only = st.checkbox("Download only audio (raw format)")
        else:
            audio_only = st.checkbox("Download only audio (raw format)", value=False)

        if audio_only:
            audio_stream = yt.streams.filter(only_audio=True)
            if len(audio_stream) == 0:
                st.error("No audio-only stream available")
                return
            audio_stream = audio_stream.first()
            
            st.subheader("Audio Download")
            st.write("This will download the audio in its original format (e.g., mp4)")
            
            if st.button("Download Audio"):
                output_path = os.path.join(os.getcwd(), "audio")
                audio_file = download_audio(audio_stream, output_path)
                
                st.success("Download complete!")
                with open(audio_file, "rb") as file:
                    st.download_button(label="Download Audio",
                                      data=file,
                                      file_name=os.path.basename(audio_file))
        else:
            if show_more_options:
                st.subheader("Video Download")
                with st.expander("Advanced options"):
                    st.write("This will download the video in the highest available quality")
                
                if st.button("Download Video"):
                    output_path = os.path.join(os.getcwd(), "video")
                    video_file = download_video(yt.streams.get_highest_resolution().first(), output_path)
                    st.success("Download complete!")
                    with open(video_file, "rb") as file:
                        st.download_button(label="Download Video",
                                          data=file,
                                          file_name=os.path.basename(video_file))
            else:
                st.subheader("Video Download")
                if st.button("Download Video"):
                    output_path = os.path.join(os.getcwd(), "video")
                    video_file = download_video(yt.streams.get_highest_resolution().first(), output_path)
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