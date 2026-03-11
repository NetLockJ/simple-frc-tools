from lib.regional_data import read_local_regionals, wrap_match_data
import matplotlib.pyplot as plt
from collections import defaultdict


if __name__ == '__main__':

    matches = read_local_regionals()

    point_deltas = defaultdict(int)

    for match in matches:
        match = wrap_match_data(match)

        if(match.is_completed):
            point_deltas[abs(match.score_delta)] += 1

    print(point_deltas)

    total_sum = sum(point_deltas.values())

    bins = list(range(0, 600, 50))
    labels = [f'{i}-{i+49}' for i in bins[:-1]]
    counts = [0] * len(labels)

    # Group data into bins
    for val, count in point_deltas.items():
        idx = val // 50
        if idx < len(counts):
            counts[idx] += count

    plt.style.use('dark_background')

    # Create plot
    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, counts, color='#0066b3', edgecolor='black')
    plt.title('Point Spread Margin')
    plt.xlabel('Point Spread Ranges')
    plt.ylabel('Total Occurances')
    plt.xticks(rotation=20)

    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_sum) * 100
        
        plt.text(bar.get_x() + bar.get_width() / 2, 
                height + 1, 
                f'{percentage:.1f}%', 
                ha='center', va='bottom')
    plt.show()


        
        

