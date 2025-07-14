# Reddit User Persona Maker using AI

[![Demo](https://img.shields.io/badge/Demo-Live-green)](https://your-deployed-link-here.com)

## What is this project?

Reddit User Persona Maker using AI is a tool that analyzes Reddit user activity and generates a persona summary using advanced language models. It leverages the Groq API for LLM-powered analysis and PRAW for Reddit data access.

## Technologies Used

- Python
- PRAW (Python Reddit API Wrapper)
- Groq API (LLM)
- Flask (or your chosen web framework)
- dotenv

## How does it work?

1. Fetches Reddit user data using PRAW.
2. Sends data to Groq LLM for persona generation.
3. Displays the generated persona summary.

## Run Locally

Follow these steps to set up and run the project on your system:

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/Reddit_User_Persona_maker_using_ai.git
    cd Reddit_User_Persona_maker_using_ai
    ```

2. **Create a Reddit App**
    - Go to [Reddit Apps](https://www.reddit.com/prefs/apps).
    - Create a new app and note the client ID, client secret, and set a custom user agent.

3. **Get your Groq API Key**
    - Sign up at [Groq](https://groq.com/) and obtain your API key.

4. **Set up your `.env` file**
    Create a `.env` file in the project root with the following content:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    REDDIT_CLIENT_ID=your_reddit_client_id
    REDDIT_CLIENT_SECRET=your_reddit_client_secret
    REDDIT_USER_AGENT=your_custom_user_agent
    ```

5. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the application**
    ```bash
    python app.py
    ```
    or
    ```bash
    python main.py
    ```


7. **Access the app**
    - Open your browser and go to `http://localhost:5000` (or the port specified).

## Demo

Try the live demo: [Demo Link](https://your-deployed-link-here.com)


