import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai():
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI works!'"}],
            max_tokens=10
        )
        print("✅ OpenAI/ChatGPT: WORKING")
        print(f"   Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print("❌ OpenAI/ChatGPT: FAILED")
        print(f"   Error: {e}")
        return False

def test_anthropic():
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say 'Claude works!'"}]
        )
        print("✅ Anthropic/Claude: WORKING")
        print(f"   Response: {response.content[0].text}")
        return True
    except Exception as e:
        print("❌ Anthropic/Claude: FAILED")
        print(f"   Error: {e}")
        return False

def test_google():
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Gemini works!'")
        print("✅ Google/Gemini: WORKING")
        print(f"   Response: {response.text}")
        return True
    except Exception as e:
        print("❌ Google/Gemini: FAILED")
        print(f"   Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing API Keys...\n")
    
    openai_ok = test_openai()
    print()
    
    anthropic_ok = test_anthropic()
    print()
    
    google_ok = test_google()
    print()
    
    working_count = sum([openai_ok, anthropic_ok, google_ok])
    print(f"📊 Summary: {working_count}/3 APIs working")
    
    if working_count > 0:
        print("🎉 Ready to generate jokes!")
    else:
        print("⚠️  No APIs working - check your keys")
