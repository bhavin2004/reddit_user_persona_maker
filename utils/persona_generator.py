from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from langchain import PromptTemplate, LLMChain

load_dotenv()
api_key = os.getenv("api-key")

llm = ChatGroq(
    model="llama3-70b-8192",
    groq_api_key=api_key , # type: ignore
    temperature=0.7
)

def persona_generator(i,data):
    print(f"⚡ Processing chunk {i+1}")
    try:
        response = llm.invoke(data)
        with open(f"prompts/response_chunk_{i+1}.txt", "w", encoding="utf-8") as f:
            f.write(response.content) # type: ignore
            print(f"Response for chunk {i+1} saved to prompts/response_chunk_{i+1}.txt") 
        return response.content
    except Exception as e:
        print(f"Error on chunk {i+1}: {e}")
        return "Error generating response"

def get_responses_in_parallel(chunks):
    with ThreadPoolExecutor(max_workers=5) as executor:
        return list(executor.map(persona_generator, range(len(chunks)), chunks))
    

def summarize_persona_chunks(chunks: list[str],username) -> str:
    """Summarizes multiple persona chunks into a final structured persona."""

    persona_template = PromptTemplate(
        input_variables=["chunks"],
        template="""
    You are a senior behavioral psychologist tasked with compiling a final Reddit user persona.

    Below are multiple persona chunks that have been generated from the user's Reddit activity:

    --- START OF CHUNKS ---
    {chunks}
    --- END OF CHUNKS ---

    Using the information above, construct a final detailed persona in the following structured format for presentation. Fill every section using the clues and insights extracted from the chunks.

    --- FINAL PERSONA TEMPLATE ---

    **Name**: (Choose a realistic name based on persona or use "Unknown")  
    **Age**: (Approximate based on content, writing style, interests)  
    **Status**: (e.g., Student, Professional, Retired, etc.)  
    **Location**: (Infer region/country if possible)  
    **Tier**: (Urban, Semi-Urban, Rural)

    **Archetype**: (e.g., The Curious Explorer, The Supportive Commentator, The Silent Observer)

    ---

    **Motivation**:  
    (Write 2–3 sentences on what motivates this user to post or comment — e.g., curiosity, self-expression, support-seeking, debate, etc.)

    ---

    **Ratings (0–5)**:
    - Convenience: #️⃣
    - Wellness: #️⃣
    - Speed: #️⃣
    - Preferences: #️⃣
    - Comfort: #️⃣
    - Dietary Needs: #️⃣

    ---

    **Personality (MBTI scale 0–5)**:
    - Introvert (0) ←——→ Extrovert (5): #️⃣  
    - Intuition (0) ←——→ Sensing (5): #️⃣  
    - Feeling (0) ←——→ Thinking (5): #️⃣  
    - Perceiving (0) ←——→ Judging (5): #️⃣  

    ---

    **Behavior**:
    - (Insightful behavior pattern from chunks)
    - (Another pattern, e.g., responds late, prefers niche subs)
    - (Behavior toward debates or emotional topics)
    - (Behavior regarding controversial content or norms)

    ---

    **Goals & Needs**:  
    (List or describe in 2–3 lines — What is the user ultimately trying to gain? Learning? Expression? Change? Fun?)

    ---

    **Frustrations**:  
    (What seems to annoy or bother them? Could be site behavior, people, topics, lack of engagement, etc.)

    ---

    Stick strictly to the format above and use citations only when appropriate. Ensure everything you write is derived logically from the chunk insights. Avoid general assumptions.
    """.strip()
    )



    # Combine all persona chunks into one text
    combined_text = "\n\n---\n\n".join(chunks)

    # Create a LangChain LLMChain
    chain = LLMChain(
        llm=llm,
        prompt=persona_template,
    )

    print("Summarizing persona chunks...")
    try:
        summary = chain.run(chunks=combined_text)

        os.makedirs("output", exist_ok=True)
        with open(f"output/{username}.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        print(f"Final summary saved: output/{username}.txt")
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Error generating summary."