import streamlit as st
import time
from utils.reddit_scrapper import fetch_user_data
from utils.prompt_generator import generate_chunked_prompts
from utils.persona_generator import get_responses_in_parallel,summarize_persona_chunks

st.title("Reddit User Persona Generator")
st.divider()
st.write("This app generates a detailed persona based on a Reddit user's posts and comments.")

input_username = st.text_input("# **Enter Reddit Username or URL**", "kojied")

if('reddit.com/' in input_username):
    #https://www.reddit.com/r/antiMLM/
    input_username = input_username.split('/')[-2]  # Extract username from URL

if st.button("Generate Persona"):
    with st.spinner("Fetching user data...",show_time=True):
        data = fetch_user_data(input_username)
    
    if not data or (not data.get("posts") and not data.get("comments")):
        st.error("No posts or comments found for this user.")
    else:
        st.success("User data fetched successfully!")
        
        with st.spinner("Generating prompts...",show_time=True):
            chunks = generate_chunked_prompts(input_username, data)
            
            if not chunks:
                st.error("No prompts generated. Please try again with a different username.")
            else:   
                st.success("Prompts generated successfully!")
                with st.spinner("Generating persona responses..."):
                    responses = get_responses_in_parallel(chunks)
                    time.sleep(60)
                    result = summarize_persona_chunks(responses, input_username)
                st.success("Persona responses generated successfully!")
                st.subheader("Final Persona Summary")
                st.code(result, language="markdown")
                st.download_button(
                    label="Download Persona Summary",
                    data=result,
                    file_name=f"{input_username}_persona_summary.txt",
                    mime="text/plain"
                )
        