import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai as genai

load_dotenv()

def test_all_models():
    prompt = "You are a professional comedy writer who also happens to be a senior software engineer.\n\nYour task:\nGenerate exactly ONE ultra-funny, clever, punchy programming quote.\n\nHard rules (must follow all):\n- Under 100 characters total\n- One single line only\n- About programming, software engineering, tech life, or AI\n- Must be witty, ironic, or absurdly clever — NOT motivational or inspirational\n- Use real developer concepts (bugs, Git, APIs, semicolons, Stack Overflow, coffee, prod, AI, etc.)\n- Clean, wholesome, and positive\n- Absolutely NO racism, sexism, sexual content, political content, hate, harassment, slurs, or offensive language\n- No violence, aggression, or negativity\n- No emojis\n- No hashtags\n- No explanations\n- No quotes around the text\n- No attribution\n- No repetition of common clichés\n\nComedy quality rules:\n- Prefer wordplay, irony, or inside jokes over slapstick\n- Should make a developer smirk or laugh, not groan\n- If the result is not genuinely funny, rewrite it until it is\n\nOutput format:\nReturn ONLY the quote text and nothing else."
    
    print("🧪 Testing all 3 AI models...\n")
    
    # Test ChatGPT
    try:
        openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        chatgpt_joke = response.choices[0].message.content.strip().strip('"')
        print(f"✅ ChatGPT: \"{chatgpt_joke}\"")
    except Exception as e:
        print(f"❌ ChatGPT failed: {e}")
    
    # Test Claude
    try:
        claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{"role": "user", "content": prompt}]
        )
        claude_joke = response.content[0].text.strip().strip('"')
        if ":" in claude_joke:
            claude_joke = claude_joke.split(":")[-1].strip()
        print(f"✅ Claude: \"{claude_joke}\"")
    except Exception as e:
        print(f"❌ Claude failed: {e}")
    
    # Test Gemini
    try:
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        gemini_joke = response.text.strip().strip('"')
        if ":" in gemini_joke:
            gemini_joke = gemini_joke.split(":")[-1].strip()
        if gemini_joke:
            gemini_joke = gemini_joke[0].upper() + gemini_joke[1:] if len(gemini_joke) > 1 else gemini_joke.upper()
        print(f"✅ Gemini: \"{gemini_joke}\"")
    except Exception as e:
        print(f"❌ Gemini failed: {e}")

if __name__ == "__main__":
    test_all_models()
