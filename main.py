import time
from utils.reddit_scrapper import fetch_user_data
from utils.prompt_generator import generate_chunked_prompts
from utils.persona_generator import get_responses_in_parallel,summarize_persona_chunks

input_username = input("Enter Reddit Username or URL: ")
if 'reddit.com/' in input_username:
    input_username = input_username.split('/')[-2]  # Extract username from URL
data = fetch_user_data(input_username)
chunks = generate_chunked_prompts(input_username, data)
responses = get_responses_in_parallel(chunks)
print(responses)
time.sleep(60) 
print(summarize_persona_chunks(responses, input_username)) # type: ignore