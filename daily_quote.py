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
                "content": "Generate a super creative, witty, and hilarious quote about programming, coding, or tech life. Be clever, punny, or absurdly funny. Keep it clean, wholesome, positive, and under 100 characters. No violence, aggression, or negativity. Think clever wordplay and programming puns."
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
            
        print("Quote updated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    update_readme_with_quote()
