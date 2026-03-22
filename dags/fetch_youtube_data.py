import os
import requests
import json
from dotenv import load_dotenv
 
dag_folder_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(dag_folder_path, '.env'))
 
youtube_api = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_data():

    # only allow unique videoIds so that video details retrieved are not duplicated
    unique_vidId = set()
    videos_retrieved = []  

    # read topic.txt
    with open(os.path.join(dag_folder_path, 'topic.txt'), 'r') as keyword:
        topic = keyword.read().strip()

    #get topic video ids
    search_url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": topic,
        "maxResults": 50,
        "type": "video",
        "key": youtube_api
    }
    
    while len(videos_retrieved) < 100:
        response = requests.get(search_url, params=params)
        search_results = response.json()
        
        video_ids = [item["id"]["videoId"] for item in search_results["items"]]
        ids_string = ",".join(video_ids)

        #get stats from video, fetch data
        stats_url = "https://www.googleapis.com/youtube/v3/videos"
        stats_params = {
            "part": "snippet,statistics",
            "id": ids_string,
            "key": youtube_api
        }

        stats_response = requests.get(stats_url, params=stats_params)
        video_stats = stats_response.json()

        for item in video_stats.get("items", []):

            if len(videos_retrieved) == 100:
                break

            video_id = item["id"]
            #ensure no videoid duplicates
            if video_id in unique_vidId: 
                continue
            unique_vidId.add(video_id)  
            
            stats = item.get("statistics", {})
            snippet = item.get("snippet", {})
            
            video = {
                "video_id": video_id,
                "title": snippet.get('title'),
                "description": snippet.get('description'),
                "number_of_views": stats.get('viewCount', 0),  
                "number_of_likes": stats.get('likeCount', 0),  
                "number_of_comments": stats.get('commentCount', 0),  
                "upload_date": snippet.get('publishedAt'),
                "video_url": f"https://www.youtube.com/watch?v={video_id}" 
            }
            
            videos_retrieved.append(video)

        if len(videos_retrieved) >= 100:
            break
        elif 'nextPageToken' in search_results:
            params["pageToken"] = search_results["nextPageToken"]
        else:
            print(f"Collected {len(videos_retrieved)} videos details.")
            break

    # save json
    json_path = os.path.join(dag_folder_path, f"{topic}.json")    
    with open(json_path, "w") as f:
        json.dump(videos_retrieved, f, indent=2) 
        print(f"{len(videos_retrieved)} videos saved to {json_path}")

if __name__ == "__main__":
    fetch_youtube_data()