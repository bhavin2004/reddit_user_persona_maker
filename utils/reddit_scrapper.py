import praw
import json
import os
from dotenv import load_dotenv
from datetime import datetime

#It is used to load the secrets information/data to runtime environment
load_dotenv()

def format_timestamp(utc):
    return datetime.utcfromtimestamp(utc).strftime('%Y-%m-%d %H:%M:%S')

#This fuction will return the instance of praw.Reddit which we will use to scrap the data of a user
def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

# Using this function to help to not get the data again and again and prevent rate limiting
def get_cache_path(username, post_limit, comment_limit):
    os.makedirs("data_cache", exist_ok=True)
    return f"data_cache/{username}_posts_{post_limit}_comments_{comment_limit}.json"
    
def fetch_user_data(username, post_limit=50, comment_limit=50):
    cache_path = get_cache_path(username, post_limit, comment_limit)
    
    if os.path.exists(cache_path):
        print(f"Loading cached data from {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            print("Cache hit!")
            data = json.load(f)
            # Return cached posts and comments
            return data
        
        
    reddit = get_reddit_instance()
    redditor  = reddit.redditor(username)
    
    posts = []
    comments = []
    
    try:
        print(f"Fetching the post upto {post_limit} of {username}......")
        
        # Fetching posts
        for submission in redditor.submissions.new(limit=post_limit):
            posts.append({
                'title':submission.title,
                "body": submission.selftext,
                'permalink': f"https://www.reddit.com{submission.permalink}",
                'score': submission.score,
                'subreddit': submission.subreddit.display_name,
                'created_utc': submission.created_utc,
                'created_at': format_timestamp(submission.created_utc)
            })
        # Fetching comments
        for comment in redditor.comments.new(limit=comment_limit):
            comments.append({
                'body': comment.body,
                'created_utc': comment.created_utc,
                'created_at': format_timestamp(comment.created_utc),
                'score': comment.score,
                'subreddit': comment.subreddit.display_name,
                'permalink': f"https://www.reddit.com{comment.permalink}"
            })
        
    except Exception as e:
        print(f"Error in fetching data of {username} and error : {e}")
    
    with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"posts": posts, "comments": comments}, f, indent=2, ensure_ascii=False)
            print(f"Data cached to {cache_path}")
    return {"posts": posts, "comments": comments}


if __name__ == "__main__":
    print("Reddit Scrapper is running...")
    print(fetch_user_data("kojied"))  # Example usage with a public user
    print("Reddit Scrapper finished running.")