import os
import json
import random
from datetime import datetime
from openai import OpenAI
import anthropic

def generate_jokes():
    """Generate jokes from different AI models"""
    jokes = {}
    
    # ChatGPT joke
    try:
        openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": "You are a professional comedy writer who also happens to be a senior software engineer.\n\nYour task:\nGenerate exactly ONE ultra-funny, clever, punchy programming quote.\n\nHard rules (must follow all):\n- Under 100 characters total\n- One single line only\n- About programming, software engineering, tech life, or AI\n- Must be witty, ironic, or absurdly clever — NOT motivational or inspirational\n- Use real developer concepts (bugs, Git, APIs, semicolons, Stack Overflow, coffee, prod, AI, etc.)\n- Clean, wholesome, and positive\n- Absolutely NO racism, sexism, sexual content, political content, hate, harassment, slurs, or offensive language\n- No violence, aggression, or negativity\n- No emojis\n- No hashtags\n- No explanations\n- No quotes around the text\n- No attribution\n- No repetition of common clichés\n\nComedy quality rules:\n- Prefer wordplay, irony, or inside jokes over slapstick\n- Should make a developer smirk or laugh, not groan\n- If the result is not genuinely funny, rewrite it until it is\n\nOutput format:\nReturn ONLY the quote text and nothing else."
            }],
            max_tokens=50
        )
        jokes['ChatGPT'] = response.choices[0].message.content.strip().strip('"')
    except:
        jokes['ChatGPT'] = "Why do programmers prefer dark mode? Because light attracts bugs!"
    
    # Claude joke (if you have Anthropic API key)
    try:
        claude_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        response = claude_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{
                "role": "user",
                "content": "Generate only a short, witty programming joke. Keep it under 80 characters. Return ONLY the joke, no extra text or explanation."
            }]
        )
        joke_text = response.content[0].text.strip().strip('"')
        # Clean up any extra text
        if ":" in joke_text:
            joke_text = joke_text.split(":")[-1].strip()
        jokes['Claude'] = joke_text
    except:
        jokes['Claude'] = "I told my computer a joke about UDP. It didn't get it."
    
    # Gemini joke
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Generate only a short, witty programming joke. Keep it under 80 characters. Return ONLY the joke, no extra text or explanation.")
        joke_text = response.text.strip().strip('"')
        # Clean up any extra text
        if ":" in joke_text:
            joke_text = joke_text.split(":")[-1].strip()
        # Capitalize first letter
        if joke_text:
            joke_text = joke_text[0].upper() + joke_text[1:] if len(joke_text) > 1 else joke_text.upper()
        jokes['Gemini'] = joke_text
        print(f"Gemini joke generated: {joke_text}")  # Debug line
    except Exception as e:
        print(f"Gemini failed: {e}")  # Debug line
        jokes['Gemini'] = "There are only 10 types of people: those who understand binary and those who don't."
    
    return jokes

def load_leaderboard():
    """Load current leaderboard from file"""
    try:
        with open('ai_leaderboard.json', 'r') as f:
            return json.load(f)
    except:
        return {
            'ChatGPT': {'votes': 0, 'wins': 0},
            'Claude': {'votes': 0, 'wins': 0},
            'Gemini': {'votes': 0, 'wins': 0}
        }

def save_leaderboard(leaderboard):
    """Save leaderboard to file"""
    with open('ai_leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=2)

def update_readme_with_jokes():
    """Update README with new jokes and voting links"""
    jokes = generate_jokes()
    leaderboard = load_leaderboard()
    
    # Create voting section
    voting_section = "## 🤖 AI Comedy Battle\n"
    voting_section += "*Come back every day for fresh AI-generated jokes to vote on! Help decide which AI has the best sense of humor.*\n\n"
    
    for ai, joke in jokes.items():
        vote_url = f"https://github.com/saagarracharla/saagarracharla/issues/new?title=Vote+for+{ai}&body=I+vote+for+{ai}%21%0A%0AJoke%3A+{joke.replace(' ', '+')}"
        voting_section += f"**{ai}:** \"{joke}\"\n"
        voting_section += f"[👍 Vote for {ai}]({vote_url})\n\n"
    
    # Add leaderboard
    voting_section += "### 🏆 AI Leaderboard\n"
    sorted_ais = sorted(leaderboard.items(), key=lambda x: x[1]['votes'], reverse=True)
    
    for ai, stats in sorted_ais:
        voting_section += f"**{ai}:** {stats['votes']} votes, {stats['wins']} daily wins\n"
    
    # Read current README
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Replace or add voting section
    voting_pattern = r'<!-- VOTING_START -->.*?<!-- VOTING_END -->'
    new_voting = f'<!-- VOTING_START -->\n{voting_section}\n<!-- VOTING_END -->'
    
    if '<!-- VOTING_START -->' in content:
        import re
        content = re.sub(voting_pattern, new_voting, content, flags=re.DOTALL)
    else:
        # Add after quote section
        quote_end = content.find('<!-- QUOTE_END -->')
        if quote_end != -1:
            insert_pos = content.find('\n', quote_end) + 1
            content = content[:insert_pos] + '\n' + new_voting + '\n' + content[insert_pos:]
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    update_readme_with_jokes()
