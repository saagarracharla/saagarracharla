import os
import re
from openai import OpenAI

def update_readme_with_quote():
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Generate a funny quote
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user", 
            "content": "You are a professional comedy writer who also happens to be a senior software engineer.

                        Your task:
                        Generate exactly ONE ultra-funny, clever, punchy programming quote.

                        Hard rules (must follow all):
                        - Under 100 characters total
                        - One single line only
                        - About programming, software engineering, tech life, or AI
                        - Must be witty, ironic, or absurdly clever — NOT motivational or inspirational
                        - Use real developer concepts (bugs, Git, APIs, semicolons, Stack Overflow, coffee, prod, AI, etc.)
                        - Clean, wholesome, and positive
                        - Absolutely NO racism, sexism, sexual content, political content, hate, harassment, slurs, or offensive language
                        - No violence, aggression, or negativity
                        - No emojis
                        - No hashtags
                        - No explanations
                        - No quotes around the text
                        - No attribution
                        - No repetition of common clichés

                        Comedy quality rules:
                        - Prefer wordplay, irony, or inside jokes over slapstick
                        - Should make a developer smirk or laugh, not groan
                        - If the result is not genuinely funny, rewrite it until it is

                        Output format:
                        Return ONLY the quote text and nothing else."
        }],
        max_tokens=50
    )
    
    quote = response.choices[0].message.content.strip().strip('"')
    quote_section = f'💬 **Daily Dev Quote**\n> "{quote}" - ChatGPT'
    
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

if __name__ == "__main__":
    update_readme_with_quote()
