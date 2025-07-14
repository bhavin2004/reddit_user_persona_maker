import os

def chunk_user_data(user_data, chunk_size=10):
    """Splits posts and comments into chunks."""
    posts = user_data.get("posts", [])
    comments = user_data.get("comments", [])
    
    chunks = []
    total = max(len(posts), len(comments))

    for i in range(0, total, chunk_size):
        chunk = {
            "posts": posts[i:i+chunk_size],
            "comments": comments[i:i+chunk_size]
        }
        chunks.append(chunk)
    
    return chunks

def generate_single_prompt(username, user_data, chunk_id=None):
    """Generates a prompt from a chunk of user data using assignment-style template."""

    instruction = f"""
You are an expert in behavioral analysis and psychology.

Your task is to generate a detailed Reddit user persona based on their public activity (posts and comments).

Follow this exact format. Fill out each section completely using behavioral evidence from the posts/comments. Cite Reddit permalinks where relevant.

--- TEMPLATE START ---

Name: {username}
Age: (Estimate based on language and topics)
Status: (Student, working professional, retired, etc.)
Location: (Guess if possible based on time zone, slang, subreddits)
Tier: (A, B, C — estimate based on engagement, tone, and subreddit type)
Archetype: (Give a single-word description, e.g., "Explorer", "Rebel", "Helper")

Motivations (Rate 1–5):
- Convenience:
- Wellness:
- Speed:
- Preferences:
- Comfort:
- Dietary Needs:

Personality (Rate 1–5 or scale positions):
- Introvert — Extrovert:
- Intuition — Sensing:
- Feeling — Thinking:
- Perceiving — Judging:

Behaviors:
- Point 1
- Point 2
- Point 3

Goals & Needs:
- [State based on topics and patterns]

Frustrations:
- [State based on complaints, tone, repeated issues]

--- END TEMPLATE ---

Below is their Reddit activity:
""".strip()

    post_block = "\n\nReddit Posts:\n"
    for post in user_data.get("posts", []):
        post_block += f"""
---
Posted: {post.get('created_at', '[N/A]')}
Subreddit: r/{post.get('subreddit', '[N/A]')}
Title: {post.get('title', '[No Title]')}
Body: {post.get('body', '[No Body]')[:500]}{"..." if len(post.get('body', '')) > 500 else ""}
Score: {post.get('score', 0)}
Link: {post.get('permalink', '[No Link]')}
"""

    comment_block = "\n\nReddit Comments:\n"
    for comment in user_data.get("comments", []):
        comment_block += f"""
---
Commented: {comment.get('created_at', '[N/A]')}
Subreddit: r/{comment.get('subreddit', '[N/A]')}
Comment: {comment.get('body', '[No Comment]')[:500]}{"..." if len(comment.get('body', '')) > 500 else ""}
Score: {comment.get('score', 0)}
Link: {comment.get('permalink', '[No Link]')}
"""

    final_prompt = f"{instruction}\n\n{post_block}\n\n{comment_block}"

    os.makedirs("prompts", exist_ok=True)
    filename = f"prompts/{username}_persona_chunk_{chunk_id}.txt" if chunk_id is not None else f"prompts/{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_prompt)

    return final_prompt


def generate_chunked_prompts(username, user_data, chunk_size=10):
    """Chunks data and generates a list of prompts."""
    chunks = chunk_user_data(user_data, chunk_size)
    prompts = []

    for i, chunk in enumerate(chunks):
        prompt = generate_single_prompt(username, chunk, chunk_id=i+1)
        prompts.append(prompt)

    return prompts
