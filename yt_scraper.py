# Importing required libraries
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import numpy as np

# Importing required variables from python files
from api_key import MY_API_KEY # You can get your own YouTube API key from the Google Developer Console website
from model import analyze_sentiment

def get_youtube_data(video_id):
    service = "youtube"
    version = "v3"
    API_KEY = MY_API_KEY

    youtube = googleapiclient.discovery.build(serviceName=service, version=version, developerKey=API_KEY)

    # Request to get video details, including like count
    video_request = youtube.videos().list(part="snippet,statistics", id=video_id)
    video_response = video_request.execute()

    # Extract like count from the video response
    like_count = video_response["items"][0]["statistics"]["likeCount"]

    # Request to get comments
    comment_request = youtube.commentThreads().list(part="snippet", videoId=video_id)
    comment_response = comment_request.execute()

    comments = []

    for item in comment_response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]
        comment_text = comment["textDisplay"]

        # Get like count for each comment
        comment_like_count = comment["likeCount"]

        comments.append([comment_text, comment_like_count])

    df = pd.DataFrame(np.array(comments), columns=["Contents", "LikeCount"])
    df["sentiment"] = df["Contents"].apply(lambda x: analyze_sentiment(x[:512]))

    return df, like_count

if __name__ == "__main__":
    with open("video_id.txt", "r") as file:
        lines = file.readlines()
        if len(lines) > 0:
            video_id = lines[0]

    df, video_like_count = get_youtube_data(video_id)
