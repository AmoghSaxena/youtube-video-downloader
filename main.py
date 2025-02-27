# Python and Streamlit Code to Download Youtube Videos.


import streamlit as st
from youtube_video_downloader import download_video

st.title("Youtube Video Downloader")
st.write("Enter the URL of the video you want to download:")





url = st.text_input("URL")

if st.button("Download"):
    st.write("Video downloaded successfully!")
    st.balloons()
    st.write("Click the Download button to download the video.")
    st.download_button(
        label="Download Video",
        data=url,
        file_name="video.mp4",
        mime="video/mp4"
    )


