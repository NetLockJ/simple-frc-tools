from datetime import datetime, timedelta
from datetime import datetime
from pathlib import Path
from frc_match import FRCMatch
import tbapy
import json

def wrap_match_data(json_dict: dict) -> FRCMatch:
    return FRCMatch.model_validate(json_dict)

def fetch_current_regionals():
    auth = ''
    current_file_path = Path(__file__).parent.resolve()
    logs_dir = current_file_path.parent

    with open(f"{logs_dir}/tba_key.txt", "r") as f:
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

    log_dir = Path(f'{__get_local_path()}')
    log_dir.mkdir(parents=True, exist_ok=True)
        
    for event in active_events:
        print(f'Logging [{event}]...')
        with open(f'{__get_local_path()}/{event}.json', 'w') as f:
            matches = tba.event_matches(str(datetime.today().year) + event, simple=False)
            json.dump(matches, f, indent=4)

def __load_local_regionals():
    dir = Path(__get_local_path())
    return [f for f in dir.iterdir() if f.is_file()]

def __get_local_path():
    current_file_path = Path(__file__).parent.resolve()
    logs_dir = current_file_path.parent / "logs" / "2026"

    return logs_dir

def read_local_regionals():
    files = __load_local_regionals()
    all_event_matches = []

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_json = json.load(f)
            
            if isinstance(raw_json, list):
                for match_data in raw_json:
                    try:
                        match_obj = FRCMatch.model_validate(match_data)
                        all_event_matches.append(match_obj)
                    except Exception as e:
                        print(f"Error parsing match in {file_path.name}: {e}")
            else:
                all_event_matches.append(FRCMatch.model_validate(raw_json))
                
    return all_event_matches

if __name__ == '__main__':
    fetch_current_regionals()