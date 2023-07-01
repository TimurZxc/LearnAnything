from googleapiclient.discovery import build

api_key = "AIzaSyDr0JKn5WlHoUqVhqj0_21JYIXyZcbS1Ck"
youtube = build("youtube", "v3", developerKey=api_key)


def get_videos(search_query: str, amount: int):
    response = youtube.search().list(
        q=search_query,
        part="id",
        type="video",
        maxResults=amount
    ).execute()

    video_ids = [item["id"]["videoId"] for item in response["items"]]
    return video_ids
