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
    leaderboard_section = "<div align=\"center\">\n\n"
    leaderboard_section += "### 🏆 AI Comedy Leaderboard 🏆\n\n"
    leaderboard_section += "| 🤖 **AI Champion** | 🗳️ **Today's Votes** | 🏆 **Days Won** | 📊 **Win Rate** |\n"
    leaderboard_section += "|:---:|:---:|:---:|:---:|\n"
    
    # Sort by daily wins first, then by total votes
    sorted_ais = sorted(leaderboard.items(), key=lambda x: (x[1]['wins'], x[1]['votes']), reverse=True)
    
    for i, (ai, stats) in enumerate(sorted_ais):
        # Add trophy emojis for top performers
        if i == 0 and stats['wins'] > 0:
            ai_display = f"🥇 **{ai}**"
        elif i == 1 and stats['wins'] > 0:
            ai_display = f"🥈 **{ai}**"
        elif i == 2 and stats['wins'] > 0:
            ai_display = f"🥉 **{ai}**"
        else:
            ai_display = f"**{ai}**"
        
        # Calculate win rate
        total_days = sum(ai_stats['wins'] for ai_stats in leaderboard.values())
        win_rate = f"{(stats['wins']/total_days*100):.0f}%" if total_days > 0 else "0%"
        
        leaderboard_section += f"| {ai_display} | {stats['votes']} | {stats['wins']} | {win_rate} |\n"
    
    leaderboard_section += "\n</div>"
    
    # Replace only the leaderboard section
    leaderboard_pattern = r'<div align="center">\s*### 🏆 AI Comedy Leaderboard 🏆.*?</div>'
    content = re.sub(leaderboard_pattern, leaderboard_section, content, flags=re.DOTALL)
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("Leaderboard updated successfully!")

if __name__ == "__main__":
    update_leaderboard_only()
