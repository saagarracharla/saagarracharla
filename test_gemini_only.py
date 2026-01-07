import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_gemini_joke():
    try:
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        print("Testing Gemini joke generation...")
        
        response = model.generate_content("Generate only a short, witty programming joke. Keep it under 80 characters. Return ONLY the joke, no extra text or explanation. Make it unique and creative, not a common joke.")
        
        print(f"Raw response: {response.text}")
        
        joke_text = response.text.strip().strip('"')
        print(f"Cleaned joke: {joke_text}")
        
        # Clean up any extra text
        if ":" in joke_text:
            joke_text = joke_text.split(":")[-1].strip()
            print(f"After colon cleanup: {joke_text}")
        
        return joke_text
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    joke = test_gemini_joke()
    if joke:
        print(f"Final joke: {joke}")
    else:
        print("Failed to generate joke")
