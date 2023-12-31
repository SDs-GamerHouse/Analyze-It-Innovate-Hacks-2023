# Importing required libraries
import streamlit as st
import validators
import importlib
import matplotlib.pyplot as plt

# Importing required python files
import yt_scraper

st.title("Analyze_It")

with st.sidebar:
    st.title("🎬 Behind the scenes of Analyze_It")
    st.write("---")
    st.subheader("Analyze_It utilizes the Hugging Face Transformers, PyTorch, and BERT machine learning model to calculate sentiment.")
    st.subheader("Analyze_It uses the YouTube API to scrape the comments of the YouTube video link the user provides")
    st.subheader("Analyze_It is made using Python (for backend) and Streamlit (for frontend)")
    st.write("---")
    st.write("©️ 2023 SDs GamerHouse [Shravan Devraj]")

st.subheader("Sentiment Analyzer for YouTube comments")
st.subheader("Know your viewers' thoughts in a click of a button")

st.write("---")

choice = st.radio("", ["Analyze YouTube comments"])

st.write("---")

if choice == "Analyze YouTube comments":
    with st.form(key="yt"):
        yt_url = st.text_input("Enter a YouTube URL")

        submitted = st.form_submit_button("Analyze_It")

        if submitted:
            if validators.url(yt_url):
                with open("video_id.txt", "w") as file:
                    video_id_index = yt_url.find("v=")
                    vid_id_start = video_id_index + 2
                    video_id = yt_url[vid_id_start:vid_id_start + 11]
                    file.write(video_id)

                # Reload the module to avoid caching issues
                importlib.reload(yt_scraper)

                @st.cache(allow_output_mutation=True)
                def load_yt_data():
                    return yt_scraper.get_youtube_data(video_id)

                cached_df, video_like_count = load_yt_data()

                def get_sentiment_summary(df):
                    sentiments = df["sentiment"].values
                    return sentiments
                
                sentiment_summary = get_sentiment_summary(cached_df)

                negative_rating = 0
                positve_rating = 0

                for rating in sentiment_summary:
                    if rating < 3:
                        negative_rating += 1
                    elif rating >= 3:
                        positve_rating += 1
                
                positive_percentage = int((positve_rating / (positve_rating + negative_rating)) * 100)
                negative_percentage = int((negative_rating / (positve_rating + negative_rating)) * 100)

                st.write(f"Positive comments: {positive_percentage}%")
                st.write(f"Negative comments: {negative_percentage}%")

                st.write(f"Video Like Count: {video_like_count}")

                # Bar chart for sentiment distribution
                fig, ax = plt.subplots()
                ax.bar(['Positive', 'Negative'], [positive_percentage, negative_percentage], color=['green', 'red'])
                ax.set_ylabel('Percentage')
                ax.set_title('Sentiment Distribution of YouTube Comments')

                # Display the percentages on top of the bars
                for i, v in enumerate([positive_percentage, negative_percentage]):
                    ax.text(i, v + 1, f'{v}%', ha='center', va='bottom')

                st.pyplot(fig)
                
                st.write(cached_df)

            else:
                st.error("❌ Invalid URL. Please enter a valid URL.")
