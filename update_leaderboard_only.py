import json
import re

def update_leaderboard_only():
    """Update only the leaderboard in README without changing jokes"""
    
    # Load current leaderboard
    try:
        with open('ai_leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
    except:
        leaderboard = {
            'ChatGPT': {'votes': 0, 'wins': 0},
            'Claude': {'votes': 0, 'wins': 0},
            'Gemini': {'votes': 0, 'wins': 0}
        }
    
    # Read current README
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Create new leaderboard table
    leaderboard_section = "### 🏆 AI Leaderboard\n\n"
    leaderboard_section += "| 🤖 AI Model | 🗳️ Total Votes | 🏆 Daily Wins |\n"
    leaderboard_section += "|-------------|----------------|---------------|\n"
    sorted_ais = sorted(leaderboard.items(), key=lambda x: x[1]['votes'], reverse=True)
    
    for ai, stats in sorted_ais:
        leaderboard_section += f"| **{ai}** | {stats['votes']} | {stats['wins']} |\n"
    
    # Replace only the leaderboard section
    leaderboard_pattern = r'### 🏆 AI Leaderboard.*?(?=\n##|\n🎵|\Z)'
    content = re.sub(leaderboard_pattern, leaderboard_section, content, flags=re.DOTALL)
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("Leaderboard updated successfully!")

if __name__ == "__main__":
    update_leaderboard_only()
