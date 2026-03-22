from regional_data import read_local_regionals, wrap_match_data
from colorama import init, Fore


if __name__ == "__main__":
    init(autoreset=True)

    matches = read_local_regionals()

    total_uncounted = 0
    total_counted = 0
    total_matches = 0

    for match in matches:
        match = wrap_match_data(match)

        if match.is_completed:
            blue_uncounted = match.score_breakdown.blue.hub_score.uncounted
            blue_hub_points = match.score_breakdown.blue.hub_score.total_count
            
            red_uncounted = match.score_breakdown.red.hub_score.uncounted
            red_hub_points = match.score_breakdown.red.hub_score.total_count
            
            total_uncounted += blue_uncounted + red_uncounted
            total_counted += blue_hub_points + red_hub_points
            
            total_matches += 1

            print(f"[{match.key}] " +
                f"{Fore.GREEN if blue_hub_points != 0 and (blue_uncounted / blue_hub_points) < 0.05 else Fore.RED} Blue Uncounted: {blue_uncounted}/{blue_hub_points}" +
                f"{Fore.GREEN if red_hub_points != 0 and (red_uncounted / red_hub_points) < 0.05 else Fore.RED} Red Uncounted: {red_uncounted}/{red_hub_points}")


print(f"\nTotal Uncounted Fuel: {total_uncounted}")
print(f"Uncounted / Match: {(total_uncounted / total_matches):.2f} | {total_uncounted}/{total_matches}")
print(f"Uncounted / Counted: {((total_uncounted / total_counted) * 100):.2f}% | {total_uncounted}/{total_counted}")
