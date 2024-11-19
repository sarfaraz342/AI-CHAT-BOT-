import cohere
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Cohere API Key from environment variable
cohere_api_key = os.getenv('COHERE_API_KEY')

# Check if API key is available
if not cohere_api_key:
    st.error("API key not found. Please set it in the environment or .env file.")
else:
    co = cohere.Client(cohere_api_key)

    # Function to get response from Cohere AI model
    def get_cohere_answer(question):
        response = co.generate(
            model='command-xlarge-nightly',  # Specify model
            prompt=question,  # Provide the input question
            max_tokens=150,  # Limit the response length
            temperature=0.7,  # Set temperature for randomness
            k=0,  # Control randomness in response
            stop_sequences=["--"],  # Stop token to end generation
            return_likelihoods='NONE'  # Do not return likelihoods
        )
        return response.generations[0].text.strip()  # Extract and return the answer

    # Streamlit page configuration
    st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Full-screen background GIF */
        .stApp {
            background-image: url('https://www.bing.com/th/id/OGC.0102fc3b3f7e09f0d0a067061641e577?pid=1.7&rurl=https%3a%2f%2fwww.commercient.com%2fwp-content%2fuploads%2f2019%2f12%2fdeepLearning.gif&ehk=Fawb41XKTsDDjTIMmpOYcF38iVXhY3w35XT7ydXNy5g%3d');  /* GIF background */
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
            height: 100vh;
        }

        /* Overlay for transparency effect */
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.5);  /* Light white overlay */
            z-index: 0;
        }

        /* Main content styling */
        .main-content {
            position: relative;
            z-index: 1;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.8);  /* Semi-transparent background */
            border-radius: 15px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
        }

        /* User input styling */
        .user-input {
            background-color: rgba(0, 123, 255, 0.1);  /* Light blue background */
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            color: #007bff;
            font-weight: bold;
        }

        /* Nexi's response box (lighter shade of neon teal) */
        .nexi-response {
            background-color: #80FFEB;  /* Lighter neon teal */
            color: #333;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
        }

        /* Title styling */
        .title {
            text-align: center;
            font-size: 40px;
            color: #00FFEF;  /* Neon teal color */
            font-family: 'Helvetica', sans-serif;
            margin-bottom: 20px;
            background-color: transparent;
            text-shadow: 
                1px 1px 0px black, 
                -1px -1px 0px black, 
                1px -1px 0px black, 
                -1px 1px 0px black, 
                2px 2px 0px black, 
                -2px -2px 0px black, 
                2px -2px 0px black, 
                -2px 2px 0px black; /* Black text border */
        }
        </style>
    """, unsafe_allow_html=True)

    # Add overlay for transparency effect
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)

    # Display title
    st.markdown("<h1 class='title main-content'>Nexi - Your AI Assistant</h1>", unsafe_allow_html=True)

    # Initialize session state for user input if not already done
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''

    # User input section with custom styling
    user_input = st.text_input("Ask a question:", key="input", placeholder="Type your question here...", label_visibility="collapsed")

    # Display Nexi's response
    if user_input:
        response = get_cohere_answer(user_input)  # Get AI response from Cohere model
        st.markdown(f"<div class='nexi-response main-content'>Nexi: {response}</div>", unsafe_allow_html=True)  # Display response
