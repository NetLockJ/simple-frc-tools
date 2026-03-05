from pathlib import Path
from datetime import datetime
import json
from colorama import init, Fore

if __name__ == "__main__":
    init(autoreset=True)
    
    dir = Path(f"./logs/{datetime.today().year}")
    files = [f for f in dir.iterdir() if f.is_file()]

    total_matches = 0
    total_auto_tele_wins = 0

    for file in files:
        with open(f'./logs/{datetime.today().year}/{file.name}', "r") as f:
            data = json.loads(f.read())

            for match in data:
                if(match["post_result_time"] != None):
                    blue_auto = match["score_breakdown"]["blue"]["totalAutoPoints"]
                    red_auto = match["score_breakdown"]["red"]["totalAutoPoints"]

                    if(blue_auto > red_auto and match["winning_alliance"] == "blue"):
                        total_auto_tele_wins += 1
                        print(f"{Fore.GREEN}[{match["key"]}] Blue Auto: {blue_auto}, Red Auto: {red_auto}, Winner: {match["winning_alliance"]}")
                    elif(red_auto > blue_auto and match["winning_alliance"] == "red"):
                        total_auto_tele_wins += 1
                        print(f"{Fore.GREEN}[{match["key"]}] Blue Auto: {blue_auto}, Red Auto: {red_auto}, Winner: {match["winning_alliance"]}")
                    else:
                         print(f"{Fore.RED}[{match["key"]}] Blue Auto: {blue_auto}, Red Auto: {red_auto}, Winner: {match["winning_alliance"]}")

                    total_matches += 1

    print(f'\nAuto to Match Win: {((total_auto_tele_wins / total_matches) * 100):.2f}%')

