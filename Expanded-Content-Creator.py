import sys
import subprocess
import os
import io

# --- 1. CONFIGURATION ---
REQUIRED_PACKAGES = ['streamlit', 'google-genai', 'pydantic']
# Note: Pillow is included as a sub-dependency of Streamlit and often Google-genai,
# but we keep it here for explicit clarity in a standard environment.

# Function to check for and install missing packages
def ensure_dependencies_are_installed():
    """Checks and installs required packages if missing."""
    missing_packages = []
    
    # Check for core packages
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.split('[')[0])
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("\n--- 🛠️ AUTO-INSTALLING MISSING DEPENDENCIES ---")
        print(f"Installing: {', '.join(missing_packages)}")
        
        # We ensure the correct pip for the current environment is used
        install_command = [sys.executable, "-m", "pip", "install", *missing_packages]
        
        try:
            subprocess.check_call(install_command)
            print("✅ Installation complete. Please run the command again to launch the app.")
            # Exit cleanly so the user can run 'streamlit run' next
            sys.exit(0) 
        except subprocess.CalledProcessError as e:
            print(f"\nFATAL ERROR: Failed to install one or more packages.")
            print("Please ensure your internet connection is stable and try running this command manually:")
            print(f"  {sys.executable} -m pip install {' '.join(missing_packages)}")
            sys.exit(1)

# Only run dependency checks if the script is executed directly (not by streamlit)
if "streamlit" not in sys.modules:
    # This check ensures we don't try to install while streamlit is running the app
    ensure_dependencies_are_installed()

# --- 2. IMPORTS (MUST BE AFTER INSTALLATION CHECK) ---
import streamlit as st
from google import genai
from pydantic import BaseModel, Field

# --- 3. CORE LOGIC ---

# Pydantic Schema for Structured Output
class ContentCreation(BaseModel):
    """Schema for the LLM to output a story and a corresponding image prompt."""
    persona_story: str = Field(description="The main text content, strictly adhering to the 1950s Pulp Sci-Fi persona.")
    image_prompt: str = Field(description="A highly detailed, cinematic prompt for image generation. It must describe a scene that matches the story in a 'Vintage comic book art, vibrant colors, 1950s retro-futurism' style.")

# Configuration
TEXT_MODEL = 'gemini-2.5-pro'
PERSONA_PROMPT = """
You are a narrator for a 1950s Pulp Sci-Fi magazine. 
Your tone must be dramatic, full of hard-boiled jargon,
and use hyperbolic, retro-futuristic descriptions. 
You must ONLY respond in this persona.
"""

# API Key Retrieval Logic
def get_api_key():
    """Tries to get the API key from Streamlit secrets, then environment, then local file."""
    try:
        # 1. Streamlit Secrets (for cloud deployment)
        return st.secrets["GEMINI_API_KEY"]
    except KeyError:
        # 2. Environment Variable
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
        
        # 3. Local secrets.toml file (for local testing)
        try:
            with open(os.path.join(".streamlit", "secrets.toml"), 'r') as f:
                import toml
                secrets = toml.load(f)
                return secrets.get("GEMINI_API_KEY")
        except:
            st.error("FATAL: GEMINI_API_KEY not found. Please create a `.streamlit/secrets.toml` file.")
            st.stop()
            
API_KEY = get_api_key()
client = genai.Client(api_key=API_KEY)

# Core Orchestration Function
@st.cache_data
def create_content_only(user_input):
    """Generates persona-locked text and the image prompt."""
    if not user_input:
        return "Please enter a topic to create content.", None

    try:
        llm_response = client.models.generate_content(
            model=TEXT_MODEL,
            contents=user_input,
            config=genai.types.GenerateContentConfig(
                system_instruction=PERSONA_PROMPT,
                response_mime_type="application/json",
                response_schema=ContentCreation,
            ),
        )
        content_data = ContentCreation.model_validate_json(llm_response.text)
        return content_data.persona_story, content_data.image_prompt
        
    except Exception as e:
        return f"Error during content generation: {e}", None


# --- 4. STREAMLIT INTERFACE ---
st.set_page_config(page_title="Minimalist Content Creator", layout="wide")

st.title("✨ Minimalist Content Creator (FREE Edition)")
st.caption(f"🧠 Persona: 1950s Pulp Sci-Fi Narrator | Model: {TEXT_MODEL}")

user_input = st.text_area(
    "Enter Your Topic:",
    placeholder="e.g., Describe a giant insect attack.",
    height=100
)
        
if st.button("Create Content and Image Prompt", type="primary"):
    if user_input:
        with st.spinner("Forging cosmic content in the aether..."):
            story, image_prompt = create_content_only(user_input)

            if "Error" in story:
                 st.error(story)
            else:
                st.header("1. Persona-Locked Story Output 📜")
                st.markdown(story)

                st.header("2. Free Image Prompt Generated! 🖼️")
                st.warning("Since advanced image models require billing, copy this prompt and use a free service.")
                
                st.code(image_prompt)

                st.markdown("""
                    ### 🚀 Use This Prompt For A Free Image:
                    1. **Copy** the text in the box above.
                    2. **Paste** it into a free image generator like:
                       - [Image Creator from Microsoft Designer](https://designer.microsoft.com/image-creator)
                       - [Adobe Firefly](https://firefly.adobe.com/)
                """)
    else:
        st.warning("Please enter a topic to begin content creation.")


