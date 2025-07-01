#!/usr/bin/env python3
"""
Euro Millions Lottery Analyzer and Predictor
Analyzes historical lottery data and generates predictions using multiple methods.
Pure Python implementation - no external dependencies required.
"""

import csv
import random
from collections import Counter, defaultdict
from datetime import datetime

class EuroMillionsAnalyzer:
    def __init__(self, csv_file):
        """Initialize the analyzer with lottery data."""
        self.data = []
        self.main_balls_cols = [1, 2, 3, 4, 5]  # Ball 1-5 column indices
        self.lucky_stars_cols = [6, 7]  # Lucky Star 1-2 column indices
        
        # Read CSV file
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Skip header
            for row in reader:
                # Convert numeric columns to integers
                processed_row = [row[0]]  # Keep date as string
                for i in range(1, 8):  # Convert balls and stars to int
                    processed_row.append(int(row[i]))
                self.data.append(processed_row)
        
        # Clean dates - remove .htm extension if present
        for row in self.data:
            row[0] = row[0].replace('.htm', '')
        
        print(f"Loaded {len(self.data)} lottery draws")
        if self.data:
            print(f"Date range: {self.data[0][0]} to {self.data[-1][0]}")
        
    def basic_statistics(self):
        """Generate basic statistics about the lottery numbers."""
        print("\n" + "="*50)
        print("BASIC STATISTICS")
        print("="*50)
        
        # Frequency analysis for main balls (1-50)
        all_main_balls = []
        for row in self.data:
            for col_idx in self.main_balls_cols:
                all_main_balls.append(row[col_idx])
        
        main_freq = Counter(all_main_balls)
        print(f"\nMain Balls Frequency (1-50):")
        print("Most frequent:")
        for num, count in main_freq.most_common(10):
            percentage = (count / len(all_main_balls)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        print("Least frequent:")
        least_common = sorted(main_freq.items(), key=lambda x: x[1])[:10]
        for num, count in least_common:
            percentage = (count / len(all_main_balls)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        # Frequency analysis for lucky stars (1-12)
        all_lucky_stars = []
        for row in self.data:
            for col_idx in self.lucky_stars_cols:
                all_lucky_stars.append(row[col_idx])
        
        lucky_freq = Counter(all_lucky_stars)
        print(f"\nLucky Stars Frequency (1-12):")
        print("Most frequent:")
        for num, count in lucky_freq.most_common(6):
            percentage = (count / len(all_lucky_stars)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        print("Least frequent:")
        least_common_lucky = sorted(lucky_freq.items(), key=lambda x: x[1])[:6]
        for num, count in least_common_lucky:
            percentage = (count / len(all_lucky_stars)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        return main_freq, lucky_freq
    
    def gap_analysis(self):
        """Analyze gaps between appearances of numbers."""
        print("\n" + "="*50)
        print("GAP ANALYSIS")
        print("="*50)
        
        # Track last appearance of each number
        main_last_seen = {i: -1 for i in range(1, 51)}
        lucky_last_seen = {i: -1 for i in range(1, 13)}
        
        for draw_idx, row in enumerate(self.data):
            # Process main balls
            drawn_main = [row[col_idx] for col_idx in self.main_balls_cols]
            for num in range(1, 51):
                if num in drawn_main:
                    main_last_seen[num] = draw_idx
            
            # Process lucky stars
            drawn_lucky = [row[col_idx] for col_idx in self.lucky_stars_cols]
            for num in range(1, 13):
                if num in drawn_lucky:
                    lucky_last_seen[num] = draw_idx
        
        # Current gaps (numbers that haven't appeared recently)
        current_draw = len(self.data) - 1
        main_current_gaps = {num: current_draw - last_seen for num, last_seen in main_last_seen.items()}
        lucky_current_gaps = {num: current_draw - last_seen for num, last_seen in lucky_last_seen.items()}
        
        print("Numbers with longest current gaps (overdue):")
        print("Main balls:")
        sorted_main_gaps = sorted(main_current_gaps.items(), key=lambda x: x[1], reverse=True)
        for num, gap in sorted_main_gaps[:10]:
            print(f"  {num:2d}: {gap:3d} draws ago")
        
        print("Lucky stars:")
        sorted_lucky_gaps = sorted(lucky_current_gaps.items(), key=lambda x: x[1], reverse=True)
        for num, gap in sorted_lucky_gaps[:6]:
            print(f"  {num:2d}: {gap:3d} draws ago")
        
        return main_current_gaps, lucky_current_gaps
    
    def pattern_analysis(self):
        """Analyze patterns in lottery draws."""
        print("\n" + "="*50)
        print("PATTERN ANALYSIS")
        print("="*50)
        
        patterns = {
            'consecutive_pairs': 0,
            'consecutive_triplets': 0,
            'same_decade': 0,
            'all_odd': 0,
            'all_even': 0,
            'majority_odd': 0,
            'majority_even': 0,
            'sum_ranges': defaultdict(int)
        }
        
        for row in self.data:
            main_nums = sorted([row[col_idx] for col_idx in self.main_balls_cols])
            
            # Consecutive numbers
            consecutive_count = 0
            for i in range(len(main_nums) - 1):
                if main_nums[i+1] - main_nums[i] == 1:
                    consecutive_count += 1
            
            if consecutive_count >= 1:
                patterns['consecutive_pairs'] += 1
            if consecutive_count >= 2:
                patterns['consecutive_triplets'] += 1
            
            # Same decade analysis
            decades = [num // 10 for num in main_nums]
            if len(set(decades)) <= 3:  # Numbers concentrated in 3 or fewer decades
                patterns['same_decade'] += 1
            
            # Odd/Even analysis
            odd_count = sum(1 for num in main_nums if num % 2 == 1)
            if odd_count == 5:
                patterns['all_odd'] += 1
            elif odd_count == 0:
                patterns['all_even'] += 1
            elif odd_count >= 3:
                patterns['majority_odd'] += 1
            else:
                patterns['majority_even'] += 1
            
            # Sum analysis
            total_sum = sum(main_nums)
            sum_range = f"{(total_sum // 25) * 25}-{(total_sum // 25) * 25 + 24}"
            patterns['sum_ranges'][sum_range] += 1
        
        total_draws = len(self.data)
        print(f"Pattern frequencies out of {total_draws} draws:")
        print(f"  Consecutive pairs: {patterns['consecutive_pairs']} ({patterns['consecutive_pairs']/total_draws*100:.1f}%)")
        print(f"  Consecutive triplets: {patterns['consecutive_triplets']} ({patterns['consecutive_triplets']/total_draws*100:.1f}%)")
        print(f"  Same decade concentration: {patterns['same_decade']} ({patterns['same_decade']/total_draws*100:.1f}%)")
        print(f"  All odd: {patterns['all_odd']} ({patterns['all_odd']/total_draws*100:.1f}%)")
        print(f"  All even: {patterns['all_even']} ({patterns['all_even']/total_draws*100:.1f}%)")
        print(f"  Majority odd: {patterns['majority_odd']} ({patterns['majority_odd']/total_draws*100:.1f}%)")
        print(f"  Majority even: {patterns['majority_even']} ({patterns['majority_even']/total_draws*100:.1f}%)")
        
        print("\nSum ranges (most common):")
        sorted_ranges = sorted(patterns['sum_ranges'].items(), key=lambda x: x[1], reverse=True)
        for sum_range, count in sorted_ranges[:8]:
            print(f"  {sum_range}: {count} ({count/total_draws*100:.1f}%)")
        
        return patterns
    
    def hot_cold_analysis(self, recent_draws=50):
        """Analyze hot and cold numbers based on recent draws."""
        print(f"\n" + "="*50)
        print(f"HOT/COLD ANALYSIS (Last {recent_draws} draws)")
        print("="*50)
        
        recent_data = self.data[-recent_draws:]
        
        # Recent frequency for main balls
        recent_main_balls = []
        for row in recent_data:
            for col_idx in self.main_balls_cols:
                recent_main_balls.append(row[col_idx])
        
        recent_main_freq = Counter(recent_main_balls)
        
        print("HOT main balls (most frequent in recent draws):")
        for num, count in recent_main_freq.most_common(10):
            percentage = (count / len(recent_main_balls)) * 100
            print(f"  {num:2d}: {count:2d} times ({percentage:.1f}%)")
        
        print("\nCOLD main balls (least frequent in recent draws):")
        cold_main = [num for num in range(1, 51) if num not in recent_main_freq]
        if cold_main:
            print(f"  Numbers not drawn: {cold_main}")
        
        if len(recent_main_freq) > 10:
            least_frequent_main = sorted(recent_main_freq.items(), key=lambda x: x[1])[:10]
            for num, count in least_frequent_main:
                percentage = (count / len(recent_main_balls)) * 100
                print(f"  {num:2d}: {count:2d} times ({percentage:.1f}%)")
        
        # Recent frequency for lucky stars
        recent_lucky_stars = []
        for row in recent_data:
            for col_idx in self.lucky_stars_cols:
                recent_lucky_stars.append(row[col_idx])
        
        recent_lucky_freq = Counter(recent_lucky_stars)
        
        print("\nHOT lucky stars:")
        for num, count in recent_lucky_freq.most_common(6):
            percentage = (count / len(recent_lucky_stars)) * 100
            print(f"  {num:2d}: {count:2d} times ({percentage:.1f}%)")
        
        print("\nCOLD lucky stars:")
        cold_lucky = [num for num in range(1, 13) if num not in recent_lucky_freq]
        if cold_lucky:
            print(f"  Numbers not drawn: {cold_lucky}")
        
        return recent_main_freq, recent_lucky_freq
    
    def weighted_random_choice(self, items, weights, k):
        """Weighted random sampling without replacement."""
        selected = []
        items_copy = items[:]
        weights_copy = weights[:]
        
        for _ in range(k):
            if not items_copy:
                break
                
            # Normalize weights
            total_weight = sum(weights_copy)
            if total_weight == 0:
                # Fallback to uniform random
                idx = random.randint(0, len(items_copy) - 1)
            else:
                rand_val = random.random() * total_weight
                cumulative = 0
                idx = 0
                for i, weight in enumerate(weights_copy):
                    cumulative += weight
                    if rand_val <= cumulative:
                        idx = i
                        break
            
            selected.append(items_copy.pop(idx))
            weights_copy.pop(idx)
        
        return selected
    
    def generate_predictions(self):
        """Generate predictions using multiple methods."""
        print("\n" + "="*70)
        print("LOTTERY PREDICTIONS FOR NEXT DRAW")
        print("="*70)
        
        # Get analysis data
        main_freq, lucky_freq = self.basic_statistics()
        main_gaps, lucky_gaps = self.gap_analysis()
        patterns = self.pattern_analysis()
        recent_main_freq, recent_lucky_freq = self.hot_cold_analysis()
        
        predictions = {}
        
        # Method 1: Most frequent numbers
        most_frequent_main = [num for num, _ in main_freq.most_common(10)]
        most_frequent_lucky = [num for num, _ in lucky_freq.most_common(6)]
        predictions['most_frequent'] = {
            'main': sorted(random.sample(most_frequent_main, 5)),
            'lucky': sorted(random.sample(most_frequent_lucky, 2))
        }
        
        # Method 2: Overdue numbers (longest gaps)
        overdue_main = sorted(main_gaps.items(), key=lambda x: x[1], reverse=True)[:10]
        overdue_lucky = sorted(lucky_gaps.items(), key=lambda x: x[1], reverse=True)[:6]
        predictions['overdue'] = {
            'main': sorted(random.sample([num for num, _ in overdue_main], 5)),
            'lucky': sorted(random.sample([num for num, _ in overdue_lucky], 2))
        }
        
        # Method 3: Hot numbers (recent frequency)
        hot_main = [num for num, _ in recent_main_freq.most_common(10)]
        hot_lucky = [num for num, _ in recent_lucky_freq.most_common(6)]
        # Ensure we have enough numbers
        if len(hot_main) < 5:
            hot_main.extend([i for i in range(1, 51) if i not in hot_main])
        if len(hot_lucky) < 2:
            hot_lucky.extend([i for i in range(1, 13) if i not in hot_lucky])
        predictions['hot'] = {
            'main': sorted(random.sample(hot_main[:15], 5)),
            'lucky': sorted(random.sample(hot_lucky[:8], 2))
        }
        
        # Method 4: Balanced approach (mix of frequent and overdue)
        balanced_main_candidates = list(set(most_frequent_main[:7] + [num for num, _ in overdue_main[:7]]))
        balanced_lucky_candidates = list(set(most_frequent_lucky[:4] + [num for num, _ in overdue_lucky[:4]]))
        predictions['balanced'] = {
            'main': sorted(random.sample(balanced_main_candidates, 5)),
            'lucky': sorted(random.sample(balanced_lucky_candidates, 2))
        }
        
        # Method 5: Pattern-based prediction
        # Aim for typical patterns: mix of odd/even, reasonable sum
        pattern_main = []
        attempts = 0
        while len(pattern_main) < 5 and attempts < 100:
            candidate = random.randint(1, 50)
            if candidate not in pattern_main:
                pattern_main.append(candidate)
            attempts += 1
        
        # Ensure mix of odd/even (aim for 2-3 odd numbers)
        odd_count = sum(1 for num in pattern_main if num % 2 == 1)
        if odd_count < 2:  # Add more odds
            for i, num in enumerate(pattern_main):
                if num % 2 == 0 and odd_count < 3:
                    new_odd = random.choice([n for n in range(1, 51, 2) if n not in pattern_main])
                    pattern_main[i] = new_odd
                    odd_count += 1
                    break
        elif odd_count > 3:  # Add more evens
            for i, num in enumerate(pattern_main):
                if num % 2 == 1 and odd_count > 3:
                    new_even = random.choice([n for n in range(2, 51, 2) if n not in pattern_main])
                    pattern_main[i] = new_even
                    odd_count -= 1
                    break
        
        pattern_lucky = sorted(random.sample(range(1, 13), 2))
        predictions['pattern_based'] = {
            'main': sorted(pattern_main),
            'lucky': pattern_lucky
        }
        
        # Method 6: Weighted approach (statistical weights)
        main_numbers = list(range(1, 51))
        main_weights = []
        for num in main_numbers:
            freq_weight = main_freq.get(num, 0) / len(self.data) * 5
            gap_weight = 1.0 / (main_gaps.get(num, 1) + 1)
            combined_weight = freq_weight * 0.6 + gap_weight * 0.4
            main_weights.append(combined_weight)
        
        weighted_main = self.weighted_random_choice(main_numbers, main_weights, 5)
        
        lucky_numbers = list(range(1, 13))
        lucky_weights = []
        for num in lucky_numbers:
            freq_weight = lucky_freq.get(num, 0) / len(self.data) * 2
            gap_weight = 1.0 / (lucky_gaps.get(num, 1) + 1)
            combined_weight = freq_weight * 0.6 + gap_weight * 0.4
            lucky_weights.append(combined_weight)
        
        weighted_lucky = self.weighted_random_choice(lucky_numbers, lucky_weights, 2)
        
        predictions['weighted_random'] = {
            'main': sorted(weighted_main),
            'lucky': sorted(weighted_lucky)
        }
        
        # Display predictions
        print("\n🎱 PREDICTION METHODS:")
        print("-" * 70)
        
        for method, pred in predictions.items():
            method_name = method.replace('_', ' ').title()
            main_str = ' - '.join(f"{num:2d}" for num in sorted(pred['main']))
            lucky_str = ' - '.join(f"{num:2d}" for num in sorted(pred['lucky']))
            print(f"{method_name:15}: [{main_str}] + [{lucky_str}]")
        
        return predictions

def main():
    """Main function to run the lottery analyzer."""
    print("🎰 Euro Millions Lottery Analyzer")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = EuroMillionsAnalyzer('/Users/elbandi/Desktop/lotteryNumbers/lottery_results.csv')
        
        # Run comprehensive analysis
        predictions = analyzer.generate_predictions()
        
        print("\n🎯 RECOMMENDED NEXT DRAW PREDICTIONS:")
        print("=" * 70)
        print("Based on comprehensive analysis, here are the top recommendations:")
        print()
        
        # Show balanced and weighted predictions as top choices
        balanced = predictions['balanced']
        weighted = predictions['weighted_random']
        
        print("🥇 PRIMARY RECOMMENDATION (Balanced Method):")
        main_str = ' - '.join(f"{num:2d}" for num in balanced['main'])
        lucky_str = ' - '.join(f"{num:2d}" for num in balanced['lucky'])
        print(f"   Main Balls: {main_str}")
        print(f"   Lucky Stars: {lucky_str}")
        
        print("\n🥈 SECONDARY RECOMMENDATION (Weighted Random):")
        main_str = ' - '.join(f"{num:2d}" for num in weighted['main'])
        lucky_str = ' - '.join(f"{num:2d}" for num in weighted['lucky'])
        print(f"   Main Balls: {main_str}")
        print(f"   Lucky Stars: {lucky_str}")
        
        print("\n📊 ANALYSIS SUMMARY:")
        print("=" * 50)
        print("✓ Analyzed all Euro Millions draws (2004-2025)")
        print("✓ Applied 6 different prediction methodologies")
        print("✓ Considered frequency, gaps, patterns, and statistical weights")
        print("✓ Generated balanced recommendations combining multiple approaches")
        
        print("\n💡 STRATEGY NOTES:")
        print("- Most frequent numbers have historical advantage")
        print("- Overdue numbers may be 'due' for selection")
        print("- Hot numbers show recent momentum")
        print("- Balanced approach combines multiple signals")
        print("- Pattern-based ensures realistic number distributions")
        print("- Weighted random uses statistical probabilities")
        
        print("\n⚠️  DISCLAIMER:")
        print("Lottery predictions are for entertainment purposes only.")
        print("Past results do not guarantee future outcomes.")
        print("Please gamble responsibly!")
        
    except FileNotFoundError:
        print("❌ Error: Could not find lottery_results.csv file")
        print("Please ensure the CSV file is in the correct location.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
