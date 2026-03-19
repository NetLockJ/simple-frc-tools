from regional_data import read_local_regionals, wrap_match_data
from colorama import init, Fore


if __name__ == "__main__":
    init(autoreset=True)

    matches = read_local_regionals()

    total_climb_rp = 0
    total_matches = 0

    for match in matches:
        
        match = wrap_match_data(match)

        if(match.is_completed):
            blue_climb_rp = match.score_breakdown.blue.traversal_achieved
            red_climb_rp = match.score_breakdown.red.traversal_achieved

            if blue_climb_rp or red_climb_rp:
                total_climb_rp += 1
                print(f'Match {Fore.GREEN}[{match.key}]: blue {blue_climb_rp}, red {red_climb_rp}')

            total_matches += 1

    print(f'\nClimb RP Percentage: {((total_climb_rp / total_matches) * 100):.2f}%')