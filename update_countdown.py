import requests
import json
from datetime import datetime, timezone
import pytz

def get_next_race():
    """Get next F1 race from 2026 calendar"""
    # 2026 F1 Calendar
    races_2026 = [
        {"name": "Australian Grand Prix", "date": "2026-03-08", "circuit": "Albert Park Circuit", "location": "Melbourne, Australia"},
        {"name": "Chinese Grand Prix", "date": "2026-03-15", "circuit": "Shanghai International Circuit", "location": "Shanghai, China"},
        {"name": "Japanese Grand Prix", "date": "2026-03-29", "circuit": "Suzuka Circuit", "location": "Suzuka, Japan"},
        {"name": "Bahrain Grand Prix", "date": "2026-04-12", "circuit": "Bahrain International Circuit", "location": "Sakhir, Bahrain"},
        {"name": "Saudi Arabian Grand Prix", "date": "2026-04-19", "circuit": "Jeddah Corniche Circuit", "location": "Jeddah, Saudi Arabia"},
        {"name": "Miami Grand Prix", "date": "2026-05-03", "circuit": "Miami International Autodrome", "location": "Miami, USA"},
        {"name": "Canadian Grand Prix", "date": "2026-05-24", "circuit": "Circuit Gilles Villeneuve", "location": "Montreal, Canada"},
        {"name": "Monaco Grand Prix", "date": "2026-06-07", "circuit": "Circuit de Monaco", "location": "Monaco"},
        {"name": "Spanish Grand Prix", "date": "2026-06-14", "circuit": "Circuit de Barcelona-Catalunya", "location": "Barcelona, Spain"},
        {"name": "Austrian Grand Prix", "date": "2026-06-28", "circuit": "Red Bull Ring", "location": "Spielberg, Austria"},
        {"name": "British Grand Prix", "date": "2026-07-05", "circuit": "Silverstone Circuit", "location": "Silverstone, UK"},
        {"name": "Belgian Grand Prix", "date": "2026-07-19", "circuit": "Circuit de Spa-Francorchamps", "location": "Spa, Belgium"},
        {"name": "Hungarian Grand Prix", "date": "2026-07-26", "circuit": "Hungaroring", "location": "Budapest, Hungary"},
        {"name": "Dutch Grand Prix", "date": "2026-08-23", "circuit": "Circuit Zandvoort", "location": "Zandvoort, Netherlands"},
        {"name": "Italian Grand Prix", "date": "2026-09-06", "circuit": "Monza Circuit", "location": "Monza, Italy"},
        {"name": "Madrid Grand Prix", "date": "2026-09-13", "circuit": "Madrid Street Circuit", "location": "Madrid, Spain"},
        {"name": "Azerbaijan Grand Prix", "date": "2026-09-26", "circuit": "Baku City Circuit", "location": "Baku, Azerbaijan"},
        {"name": "Singapore Grand Prix", "date": "2026-10-11", "circuit": "Marina Bay Street Circuit", "location": "Singapore"},
        {"name": "United States Grand Prix", "date": "2026-10-25", "circuit": "Circuit of the Americas", "location": "Austin, USA"},
        {"name": "Mexico City Grand Prix", "date": "2026-11-01", "circuit": "Autódromo Hermanos Rodríguez", "location": "Mexico City, Mexico"},
        {"name": "São Paulo Grand Prix", "date": "2026-11-08", "circuit": "Interlagos Circuit", "location": "São Paulo, Brazil"},
        {"name": "Las Vegas Grand Prix", "date": "2026-11-22", "circuit": "Las Vegas Street Circuit", "location": "Las Vegas, USA"},
        {"name": "Qatar Grand Prix", "date": "2026-11-29", "circuit": "Lusail International Circuit", "location": "Lusail, Qatar"},
        {"name": "Abu Dhabi Grand Prix", "date": "2026-12-06", "circuit": "Yas Marina Circuit", "location": "Abu Dhabi, UAE"}
    ]
    
    now = datetime.now(timezone.utc)
    
    for race in races_2026:
        # Assume races start at 14:00 UTC (typical F1 race time)
        race_datetime = datetime.fromisoformat(f"{race['date']}T14:00:00+00:00")
        if race_datetime > now:
            return {
                'raceName': race['name'],
                'date': race['date'],
                'time': '14:00:00Z',
                'Circuit': {
                    'circuitName': race['circuit'],
                    'Location': {
                        'locality': race['location'].split(', ')[0],
                        'country': race['location'].split(', ')[-1]
                    }
                }
            }
    
    return None

def calculate_countdown(race_datetime):
    """Calculate time remaining until race"""
    now = datetime.now(timezone.utc)
    diff = race_datetime - now
    
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    return days, hours, minutes

def update_readme():
    """Update README with F1 countdown"""
    race = get_next_race()
    
    if not race:
        countdown_text = "🏎️ **F1 Season Complete!** See you next year!"
    else:
        race_datetime = datetime.fromisoformat(f"{race['date']}T{race['time'][:-1]}+00:00")
        days, hours, minutes = calculate_countdown(race_datetime)
        
        countdown_text = f"""🏎️ **Next F1 Race: {race['raceName']}**
⏰ {days} days, {hours} hours, {minutes} minutes
📍 {race['Circuit']['circuitName']}
🌍 {race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}"""
    
    # Read current README
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Replace countdown section
    start_marker = "<!-- F1_COUNTDOWN_START -->"
    end_marker = "<!-- F1_COUNTDOWN_END -->"
    
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = f"{before}{start_marker}\n{countdown_text}\n{end_marker}{after}"
    else:
        # Add countdown section at the top
        new_content = f"{start_marker}\n{countdown_text}\n{end_marker}\n\n{content}"
    
    # Write updated README
    with open('README.md', 'w') as f:
        f.write(new_content)
    
    print(f"Updated README with F1 countdown")

if __name__ == "__main__":
    update_readme()
