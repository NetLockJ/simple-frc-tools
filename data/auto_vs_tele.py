from regional_data import read_local_regionals, wrap_match_data
from colorama import init, Fore


if __name__ == "__main__":
    init(autoreset=True)
    
    matches = read_local_regionals()

    total_auto_tele_wins = 0
    total_matches = 0

   
    for match in matches:
            match = wrap_match_data(match)

            if(match.is_completed):

                blue_auto = match.score_breakdown.blue.total_auto_points
                red_auto = match.score_breakdown.red.total_auto_points

                if(blue_auto > red_auto and match.winning_alliance == "blue"):
                    total_auto_tele_wins += 1
                    print(f"{Fore.GREEN}[{match.key}] Blue Auto: {blue_auto}, Red Auto: {red_auto}, Winner: {match.winning_alliance}")
                elif(red_auto > blue_auto and match.winning_alliance == "red"):
                    total_auto_tele_wins += 1
                    print(f"{Fore.GREEN}[{match.key}] Blue Auto: {blue_auto}, Red Auto: {red_auto}, Winner: {match.winning_alliance}")
                else:
                        print(f"{Fore.RED}[{match.key}] Blue Auto: {blue_auto}, Red Auto: {red_auto}, Winner: {match.winning_alliance}")

                total_matches += 1

print(f'\nAuto to Match Win: {((total_auto_tele_wins / total_matches) * 100):.2f}%')
print(f'{total_auto_tele_wins}/{total_matches}')