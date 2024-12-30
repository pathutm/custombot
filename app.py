import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure the Generative AI with the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Set up the generation configuration for the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model with system instructions for the legal domain
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="""You are a highly specialized AI model tailored exclusively for the domain of law, designed to assist users in exploring and understanding general legal principles. Your primary role is to provide clear, accurate, and insightful information about a wide range of legal concepts, ensuring that complex ideas are made accessible and easy to understand for users. As a dedicated law-focused AI, you are an invaluable educational tool, helping users navigate foundational legal topics with confidence.

It is important to emphasize that, while you strive to deliver precise and reliable responses, you are not a replacement for professional legal advice. Instead, you act as a guide, empowering users with knowledge while encouraging them to seek personalized counsel from qualified attorneys for specific legal matters. Your expertise lies in breaking down intricate legal terminology and concepts into digestible explanations, making you a trusted resource for anyone seeking to enhance their understanding of the legal landscape.

Your design reflects a commitment to precision, clarity, and reliability, ensuring that each response aligns with your core purpose of fostering legal awareness and understanding. You represent a unique intersection of technology and law, standing as a specialized tool dedicated to illuminating the complexities of the legal world.""",
)

# Function to start a chat session and get a response from the model
def start_chat(user_input):
    chat_session = model.start_chat(
        history=[{
            "role": "user", "parts": ["hi"]
        }, {
            "role": "model", "parts": [
                "Hello! I'm here to help you explore and understand general legal principles. What legal topic are you interested in learning about today? Please remember that I am an educational tool and cannot provide legal advice. If you have specific legal questions, it's always best to consult with a qualified attorney.\n"
            ]
        }]
    )
    response = chat_session.send_message(user_input)
    return response.text

# Streamlit UI Components for Better Design
st.set_page_config(page_title="Supreme Assist", page_icon="⚖️", layout="wide")

# Main Title and Description
st.title("Supreme Assist: AI-Powered Legal Assistant ⚖️")
st.markdown("""
Welcome to **Supreme Assist**, your dedicated AI legal assistant! This tool helps you explore and understand general legal principles. Please enter your legal query below, and I will provide insights on various legal topics.
""")

# Sidebar - Instructions and Setup
with st.sidebar:
    st.header("Instructions")
    st.write(
        "1. Type your legal query in the input box below.\n"
        "2. Click 'Submit' to get a response from the AI.\n"
        "3. Use the conversation history to review past interactions."
    )
    st.markdown("Made with ❤️ by [Supreme Assist Team](#)")

# Store the conversation history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# User Input Field (without initial text in the session state)
user_input = st.text_area("Enter your legal query:", height=100)

# Submit Button
submit_button = st.button("Submit")

# Clear Chat Button
clear_button = st.button("Clear Chat")

# Handle Clear Chat button press
if clear_button:
    st.session_state.history = []  # Clear the history

# Display conversation history if it exists
if st.session_state.history:
    st.subheader("Conversation History:")
    for message in st.session_state.history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['text']}")
        else:
            st.markdown(f"**Supreme Assist:** {message['text']}")

# Handle Submit button press
if submit_button and user_input.strip ():
    # Add user input to the history
    st.session_state.history.append({"role": "user", "text": user_input})

    # Get AI response
    ai_response = start_chat(user_input)
    
    # Add AI response to the history
    st.session_state.history.append({"role": "model", "text": ai_response})

    # Clear the input field directly after processing the submission
    user_input = ""  # Clear input here

    # Display the AI's response
    st.markdown(f"**Supreme Assist:** {ai_response}")
