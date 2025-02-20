from crewai.flow.flow import Flow, start, listen, router
from litellm import completion
import os 
import dotenv
import streamlit as st

# Load environment variables
dotenv.load_dotenv()

# Set page configuration for a wide layout and custom title
st.set_page_config(page_title="Content Generator", layout="wide")

# Inject custom CSS styles into the app
st.markdown(
    """
    <style>
    /* Change overall background */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Style the title */
    h1 {
        color: #4CAF50;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
    }
    /* Style text input boxes */
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
    }
    /* Style download button */
    .stDownloadButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stDownloadButton button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Content Generator")
API_KEY = os.getenv('GEMINI_API_KEY')

class ContentGenrator(Flow):
    @start()
    def content_generator(self):
        user = st.text_input("Enter title of the content...")
        self.state["user"] = user
    
    @router(content_generator)
    def correct_content_tittle(self):
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze the following title/phrase: '{self.state['user']}'

Task: Determine if this is a meaningful phrase or title that can be expanded upon.

Instructions:
- If the input is a recognizable word, phrase, or concept that you can explain or elaborate on, respond with 'found'
- If the input is gibberish, random characters, or completely nonsensical, respond with 'not_found'
- Respond with ONLY 'found' or 'not_found' - no other text

Example responses:
- For 'artificial intelligence' → 'found'
- For 'asdf123xyz' → 'not_found'"""
                }
            ]
        )
        result = response["choices"][0]["message"]["content"].strip().lower()
        if result == "found":
            return "found"
        else:
            return "not_found"
         
    @listen("found")
    def generate_content(self):
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a content for {self.state['user']}"
                }
            ]
        )
        content = response["choices"][0]["message"]["content"].strip()
        st.write(content)
        self.state["result"] = content
        return "generate_content"
    
    @listen("not_found")
    def error(self):
        st.write("Invalid title/phrase. Please try again.")
    
    @listen("generate_content")
    def download_content(self):
        if "result" in self.state:
            content = self.state["result"]
            title = self.state["user"]
            st.download_button(
                label="Download Content",
                data=content,
                file_name=f"{title}.txt",
                mime="text/plain"
            )

def kickoff():
    flow = ContentGenrator()
    flow.kickoff()

kickoff()
