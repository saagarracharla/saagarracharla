import os
import re
from openai import OpenAI

def update_readme_with_quote():
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Generate a funny quote
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": "You are a professional comedy writer who also happens to be a senior software engineer.\n\nYour task:\nGenerate exactly ONE ultra-funny, clever, punchy programming quote.\n\nHard rules (must follow all):\n- Under 100 characters total\n- One single line only\n- About programming, software engineering, tech life, or AI\n- Must be witty, ironic, or absurdly clever — NOT motivational or inspirational\n- Use real developer concepts (bugs, Git, APIs, semicolons, Stack Overflow, coffee, prod, AI, etc.)\n- Clean, wholesome, and positive\n- Absolutely NO racism, sexism, sexual content, political content, hate, harassment, slurs, or offensive language\n- No violence, aggression, or negativity\n- No emojis\n- No hashtags\n- No explanations\n- No quotes around the text\n- No attribution\n- No repetition of common clichés\n\nComedy quality rules:\n- Prefer wordplay, irony, or inside jokes over slapstick\n- Should make a developer smirk or laugh, not groan\n- If the result is not genuinely funny, rewrite it until it is\n\nOutput format:\nReturn ONLY the quote text and nothing else."
            }],
            max_tokens=50
        )
        
        quote = response.choices[0].message.content.strip().strip('"')
        quote_section = f'### 💬 Daily Dev Quote\n_Fresh programming humor delivered daily — because we all need a laugh between merge conflicts_\n\n> **{quote}** — ChatGPT'
        
        # Read current README
        with open('README.md', 'r') as f:
            content = f.read()
        
        # Replace or add quote section
        quote_pattern = r'<!-- QUOTE_START -->.*?<!-- QUOTE_END -->'
        new_quote = f'<!-- QUOTE_START -->\n{quote_section}\n<!-- QUOTE_END -->'
        
        if '<!-- QUOTE_START -->' in content:
            content = re.sub(quote_pattern, new_quote, content, flags=re.DOTALL)
        else:
            # Add after F1 countdown
            f1_end = content.find('<!-- F1_COUNTDOWN_END -->')
            if f1_end != -1:
                insert_pos = content.find('\n', f1_end) + 1
                content = content[:insert_pos] + '\n' + new_quote + '\n' + content[insert_pos:]
        
        # Write updated README
        with open('README.md', 'w') as f:
            f.write(content)
            
        print("Quote updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    update_readme_with_quote()
