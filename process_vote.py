import json
import sys

def process_vote(issue_title, voter):
    """Process a vote from GitHub issue"""
    
    # Extract AI name from issue title
    ai_name = None
    if "Vote for ChatGPT" in issue_title:
        ai_name = "ChatGPT"
    elif "Vote for Claude" in issue_title:
        ai_name = "Claude"
    elif "Vote for Gemini" in issue_title:
        ai_name = "Gemini"
    
    if not ai_name:
        return
    
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
    
    # Add vote
    if ai_name in leaderboard:
        leaderboard[ai_name]['votes'] += 1
    
    # Save updated leaderboard
    with open('ai_leaderboard.json', 'w') as f:
        json.dump(leaderboard, f, indent=2)
    
    print(f"Vote recorded for {ai_name} by {voter}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        process_vote(sys.argv[1], sys.argv[2])
