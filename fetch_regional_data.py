from datetime import datetime, timedelta
from pathlib import Path
import tbapy
import json

if __name__ == "__main__":
    auth = ''
    with open("tba_key.txt", "r") as f:
        auth = f.readline()

    tba = tbapy.TBA(auth)
    events = tba.events(datetime.today().year)

    active_events = []

    for event in events:
        start = datetime.strptime(event['start_date'], "%Y-%m-%d")
        end =  datetime.strptime(event['end_date'], "%Y-%m-%d")

        # Has event started, past practice day, and is a regional?
        if start + timedelta(days=1) <= datetime.today() and event['event_type_string'] == "Regional":
            active_events.append(event['event_code'])

    log_dir = Path(f'logs/{datetime.today().year}')
    log_dir.mkdir(parents=True, exist_ok=True)
        
    for event in active_events:
        print(f'Logging [{event}]...')
        with open(f'logs/{datetime.today().year}/{event}.json', 'w') as f:
            matches = tba.event_matches(str(datetime.today().year) + event, simple=False)
            json.dump(matches, f, indent=4)



