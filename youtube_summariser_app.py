import streamlit as st
from youtube_summariser import get_video_summary

# to run the app: streamlit run youtube_summariser_app.py

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    elif "youtube.com" in url:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
    return url  # Return as-is if it's already just the ID

st.set_page_config(
    page_title="Tennis Video Summarizer",
    page_icon="🎾",
    layout="wide"
)

st.title("🎾 Tennis Video Summarizer")

# Input section
st.subheader("Enter YouTube Video")
video_url = st.text_input(
    "Enter YouTube URL or Video ID",
    placeholder="https://youtube.com/watch?v=... or video_id"
)

if st.button("Summarize Video", type="primary"):
    if video_url:
        with st.spinner("Analyzing video..."):
            try:
                # Extract video ID and get summary
                video_id = extract_video_id(video_url)
                summary = get_video_summary(video_id)
                
                # Display results
                st.success("Summary generated successfully!")
                st.markdown("### Summary")
                st.markdown(summary)
                
                # Display video
                st.markdown("### Video")
                st.video(f"https://youtube.com/watch?v={video_id}")
                
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")
    else:
        st.warning("Please enter a YouTube URL or video ID")

# Footer
st.markdown("---")
st.markdown(
    "Made by the Rakket AI Team| "
    "Powered by YouTube API & Google Gemini"
) 