#!/usr/bin/env python3
"""Test script for AI Comedy Battle APIs"""

import os
from dotenv import load_dotenv
import openai
from anthropic import Anthropic
import google.genai as genai

load_dotenv()

def test_openai():
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'OpenAI works!'"}],
            max_tokens=10
        )
        return True, response.choices[0].message.content.strip()
    except Exception as e:
        return False, str(e)

def test_anthropic():
    try:
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say 'Claude works!'"}]
        )
        return True, response.content[0].text.strip()
    except Exception as e:
        return False, str(e)

def test_gemini():
    try:
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',
            contents="Say 'Gemini works!'"
        )
        return True, response.text.strip()
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("🧪 Testing AI Comedy Battle APIs...\n")
    
    tests = [
        ("OpenAI/ChatGPT", test_openai),
        ("Anthropic/Claude", test_anthropic),
        ("Google/Gemini", test_gemini)
    ]
    
    working_count = 0
    for name, test_func in tests:
        success, result = test_func()
        if success:
            print(f"✅ {name}: WORKING")
            print(f"   Response: {result}")
            working_count += 1
        else:
            print(f"❌ {name}: FAILED")
            print(f"   Error: {result}")
        print()
    
    print(f"📊 Summary: {working_count}/3 APIs working")
    if working_count >= 2:
        print("🎉 Ready to generate jokes!")
