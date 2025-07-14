import time
from utils.reddit_scrapper import fetch_user_data
from utils.prompt_generator import generate_chunked_prompts
from utils.persona_generator import get_responses_in_parallel,summarize_persona_chunks

data = fetch_user_data("kojied")
chunks = generate_chunked_prompts("kojied", data)
responses = get_responses_in_parallel(chunks)
print(responses)
time.sleep(60)  # Simulate some processing time
print(summarize_persona_chunks(responses)) # type: ignore