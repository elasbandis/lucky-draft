#!/usr/bin/env python3
"""
Euro Millions Lottery Analyzer and Predictor - Quick Version
"""

import csv
import random
from collections import Counter

def analyze_lottery():
    print("🎰 Euro Millions Lottery Analyzer")
    print("=" * 50)
    
    # Read lottery data
    data = []
    with open('lottery_results.csv', 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip header
        for row in reader:
            data.append([row[0]] + [int(x) for x in row[1:8]])
    
    print(f"✓ Loaded {len(data)} lottery draws")
    print(f"✓ Date range: {data[0][0]} to {data[-1][0]}")
    
    # Extract all main balls and lucky stars
    all_main_balls = []
    all_lucky_stars = []
    
    for row in data:
        all_main_balls.extend(row[1:6])  # Ball 1-5
        all_lucky_stars.extend(row[6:8])  # Lucky Star 1-2
    
    # Frequency analysis
    main_freq = Counter(all_main_balls)
    lucky_freq = Counter(all_lucky_stars)
    
    print("\n📊 FREQUENCY ANALYSIS")
    print("=" * 30)
    print("Most frequent main balls:")
    for num, count in main_freq.most_common(10):
        print(f"  {num:2d}: {count} times ({count/len(all_main_balls)*100:.1f}%)")
    
    print("\nMost frequent lucky stars:")
    for num, count in lucky_freq.most_common(6):
        print(f"  {num:2d}: {count} times ({count/len(all_lucky_stars)*100:.1f}%)")
    
    # Gap analysis (overdue numbers)
    main_last_seen = {i: -1 for i in range(1, 51)}
    lucky_last_seen = {i: -1 for i in range(1, 13)}
    
    for draw_idx, row in enumerate(data):
        for num in row[1:6]:  # Main balls
            main_last_seen[num] = draw_idx
        for num in row[6:8]:  # Lucky stars
            lucky_last_seen[num] = draw_idx
    
    current_draw = len(data) - 1
    main_gaps = {num: current_draw - last_seen for num, last_seen in main_last_seen.items()}
    lucky_gaps = {num: current_draw - last_seen for num, last_seen in lucky_last_seen.items()}
    
    print("\n⏰ OVERDUE ANALYSIS")
    print("=" * 30)
    print("Most overdue main balls:")
    sorted_main_gaps = sorted(main_gaps.items(), key=lambda x: x[1], reverse=True)
    for num, gap in sorted_main_gaps[:10]:
        print(f"  {num:2d}: {gap} draws ago")
    
    print("\nMost overdue lucky stars:")
    sorted_lucky_gaps = sorted(lucky_gaps.items(), key=lambda x: x[1], reverse=True)
    for num, gap in sorted_lucky_gaps[:6]:
        print(f"  {num:2d}: {gap} draws ago")
    
    # Hot numbers (recent 50 draws)
    recent_data = data[-50:]
    recent_main = []
    recent_lucky = []
    
    for row in recent_data:
        recent_main.extend(row[1:6])
        recent_lucky.extend(row[6:8])
    
    recent_main_freq = Counter(recent_main)
    recent_lucky_freq = Counter(recent_lucky)
    
    print("\n🔥 HOT NUMBERS (Last 50 draws)")
    print("=" * 30)
    print("Hottest main balls:")
    for num, count in recent_main_freq.most_common(10):
        print(f"  {num:2d}: {count} times ({count/len(recent_main)*100:.1f}%)")
    
    print("\nHottest lucky stars:")
    for num, count in recent_lucky_freq.most_common(6):
        print(f"  {num:2d}: {count} times ({count/len(recent_lucky)*100:.1f}%)")
    
    # Generate predictions
    print("\n🎯 PREDICTIONS FOR NEXT DRAW")
    print("=" * 50)
    
    # Method 1: Most frequent
    frequent_main = [num for num, _ in main_freq.most_common(10)]
    frequent_lucky = [num for num, _ in lucky_freq.most_common(6)]
    pred1_main = sorted(random.sample(frequent_main, 5))
    pred1_lucky = sorted(random.sample(frequent_lucky, 2))
    
    # Method 2: Overdue numbers
    overdue_main = [num for num, _ in sorted_main_gaps[:10]]
    overdue_lucky = [num for num, _ in sorted_lucky_gaps[:6]]
    pred2_main = sorted(random.sample(overdue_main, 5))
    pred2_lucky = sorted(random.sample(overdue_lucky, 2))
    
    # Method 3: Hot numbers
    hot_main = [num for num, _ in recent_main_freq.most_common(10)]
    hot_lucky = [num for num, _ in recent_lucky_freq.most_common(6)]
    if len(hot_main) < 5:
        hot_main.extend([i for i in range(1, 51) if i not in hot_main])
    if len(hot_lucky) < 2:
        hot_lucky.extend([i for i in range(1, 13) if i not in hot_lucky])
    pred3_main = sorted(random.sample(hot_main[:15], 5))
    pred3_lucky = sorted(random.sample(hot_lucky[:8], 2))
    
    # Method 4: Balanced (mix of frequent and overdue)
    balanced_main = list(set(frequent_main[:7] + overdue_main[:7]))
    balanced_lucky = list(set(frequent_lucky[:4] + overdue_lucky[:4]))
    pred4_main = sorted(random.sample(balanced_main, 5))
    pred4_lucky = sorted(random.sample(balanced_lucky, 2))
    
    # Method 5: Random with constraints
    pred5_main = []
    while len(pred5_main) < 5:
        num = random.randint(1, 50)
        if num not in pred5_main:
            pred5_main.append(num)
    pred5_main.sort()
    pred5_lucky = sorted(random.sample(range(1, 13), 2))
    
    # Display predictions
    predictions = [
        ("Most Frequent", pred1_main, pred1_lucky),
        ("Overdue Numbers", pred2_main, pred2_lucky),
        ("Hot Numbers", pred3_main, pred3_lucky),
        ("Balanced Mix", pred4_main, pred4_lucky),
        ("Smart Random", pred5_main, pred5_lucky)
    ]
    
    for i, (method, main, lucky) in enumerate(predictions, 1):
        main_str = " - ".join(f"{num:2d}" for num in main)
        lucky_str = " - ".join(f"{num:2d}" for num in lucky)
        print(f"{i}. {method:14}: [{main_str}] + [{lucky_str}]")
    
    print("\n🏆 TOP RECOMMENDATIONS")
    print("=" * 50)
    
    print("🥇 PRIMARY PICK (Balanced Mix):")
    main_str = " - ".join(f"{num:2d}" for num in pred4_main)
    lucky_str = " - ".join(f"{num:2d}" for num in pred4_lucky)
    print(f"   Main Balls: {main_str}")
    print(f"   Lucky Stars: {lucky_str}")
    
    print("\n🥈 SECONDARY PICK (Most Frequent):")
    main_str = " - ".join(f"{num:2d}" for num in pred1_main)
    lucky_str = " - ".join(f"{num:2d}" for num in pred1_lucky)
    print(f"   Main Balls: {main_str}")
    print(f"   Lucky Stars: {lucky_str}")
    
    print("\n📈 ANALYSIS COMPLETE!")
    print("=" * 50)
    print(f"✓ Analyzed {len(data)} Euro Millions draws")
    print("✓ Applied 5 prediction methodologies")
    print("✓ Generated statistically-informed picks")
    print("\n⚠️  Remember: This is for entertainment only!")
    print("   Past results don't guarantee future outcomes.")

if __name__ == "__main__":
    analyze_lottery()
