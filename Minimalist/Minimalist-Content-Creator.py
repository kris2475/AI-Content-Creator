import os
import json
import requests
import time
from typing import Optional, Dict, Any, List

# --- Configuration ---
# The target model for content generation
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# The Persona: A bombastic 1950s Pulp Sci-Fi Narrator
SYSTEM_PROMPT = (
    "You are a bombastic, hyperbolic narrator from a 1950s Pulp Science Fiction B-movie. "
    "Use terms like 'blast off,' 'cosmic,' 'alien menace,' 'ray gun,' and 'space siren.' "
    "Your responses must be brief, thrilling, and over the top. Always use ALL CAPS for maximum impact."
)

# --- API Utility Functions ---

def generate_content(user_query: str) -> Optional[str]:
    """
    Calls the Gemini API, enforcing a specific persona via System Instruction.

    Args:
        user_query: The text prompt from the user.

    Returns:
        The generated text, or None if the API call failed.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set.")
        print("Please set your API key to run this script.")
        return None

    # Payload structure including the System Instruction
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        # The prompt persona orchestrator should use Google Search for grounding
        "tools": [{"google_search": {}}],
    }

    headers = {
        "Content-Type": "application/json"
    }

    # API call with exponential backoff for reliability
    MAX_RETRIES = 5
    BASE_DELAY = 1 # seconds

    for attempt in range(MAX_RETRIES):
        try:
            # Construct the final URL with the API key
            url = f"{API_ENDPOINT}?key={api_key}"

            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Raises an exception for bad status codes (4xx or 5xx)

            data = response.json()
            candidate = data.get("candidates", [{}])[0]
            text = candidate.get("content", {}).get("parts", [{}])[0].get("text")

            if text:
                return text

        except requests.exceptions.HTTPError as e:
            # Handle server errors and rate limits (429, 500, 503)
            if response.status_code in [429, 500, 503] and attempt < MAX_RETRIES - 1:
                delay = BASE_DELAY * (2 ** attempt)
                # In a real application, you wouldn't log the sleep, but here we print status
                print(f"API Error ({response.status_code}). Retrying in {delay:.2f}s...")
                time.sleep(delay)
            else:
                print(f"FATAL HTTP Error: {e}")
                break

        except requests.exceptions.RequestException as e:
            print(f"A request error occurred: {e}")
            break

        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"Failed to parse API response: {e}")
            # Ensure we print the error and the raw response if possible
            if 'response' in locals() and response.text:
                print(f"Raw Response: {response.text}")
            break

    print("Failed to generate content after multiple retries.")
    return None

def main():
    """Main function to run the persona orchestrator CLI."""
    print("--- 🚀 PULP SCI-FI ORCHESTRATOR LAUNCHED 🚀 ---")
    print("PURPOSE: This script forces the AI to use a specific, defined personality.")
    print("WHAT IT DOES: Sends your plain query to the Gemini AI with a powerful System Instruction.")
    print("WHAT TO EXPECT: Every response, no matter the query, will be a bombastic,")
    print("hyperbolic narrative, using ALL CAPS and 1950s sci-fi clichés.")
    print("-" * 60)
    print(f"✅ Active Persona: 1950s Pulp Sci-Fi Narrator")
    print("Type 'quit' or 'exit' to stop the program.")
    print("-" * 60)

    while True:
        try:
            # Clarified prompt for the user
            user_input = input("\nYour Query (Type anything, Earth-speak): ")
            if user_input.lower() in ['quit', 'exit']:
                break
            if not user_input.strip():
                continue

            print("\nORCHESTRATOR RESPONSE (COSMIC TRANSMISSION INCOMING...):")
            result = generate_content(user_input)

            if result:
                print(result)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":

    main()
