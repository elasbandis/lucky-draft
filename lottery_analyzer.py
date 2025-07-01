#!/usr/bin/env python3
"""
Euro Millions Lottery Analyzer and Predictor
Analyzes historical lottery data and generates predictions using multiple methods.
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class EuroMillionsAnalyzer:
    def __init__(self, csv_file):
        """Initialize the analyzer with lottery data."""
        self.df = pd.read_csv(csv_file)
        self.main_balls = ['Ball 1', 'Ball 2', 'Ball 3', 'Ball 4', 'Ball 5']
        self.lucky_stars = ['Lucky Star 1', 'Lucky Star 2']
        
        # Clean the data - some dates might have .htm extension
        self.df['Date'] = self.df['Date'].astype(str).str.replace('.htm', '')
        
        print(f"Loaded {len(self.df)} lottery draws")
        print(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        
    def basic_statistics(self):
        """Generate basic statistics about the lottery numbers."""
        print("\n" + "="*50)
        print("BASIC STATISTICS")
        print("="*50)
        
        # Frequency analysis for main balls (1-50)
        all_main_balls = []
        for col in self.main_balls:
            all_main_balls.extend(self.df[col].tolist())
        
        main_freq = Counter(all_main_balls)
        print(f"\nMain Balls Frequency (1-50):")
        print("Most frequent:")
        for num, count in main_freq.most_common(10):
            percentage = (count / len(all_main_balls)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        print("Least frequent:")
        for num, count in main_freq.most_common()[-10:]:
            percentage = (count / len(all_main_balls)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        # Frequency analysis for lucky stars (1-12)
        all_lucky_stars = []
        for col in self.lucky_stars:
            all_lucky_stars.extend(self.df[col].tolist())
        
        lucky_freq = Counter(all_lucky_stars)
        print(f"\nLucky Stars Frequency (1-12):")
        print("Most frequent:")
        for num, count in lucky_freq.most_common(6):
            percentage = (count / len(all_lucky_stars)) * 100
            print(f"  {num:2d}: {count:3d} times ({percentage:.1f}%)")
        
        print("Least frequent:")
        for num, count in lucky_freq.most_common()[-6:]:
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
        
        main_gaps = {i: [] for i in range(1, 51)}
        lucky_gaps = {i: [] for i in range(1, 13)}
        
        for draw_idx, row in self.df.iterrows():
            # Process main balls
            drawn_main = [row[col] for col in self.main_balls]
            for num in range(1, 51):
                if num in drawn_main:
                    if main_last_seen[num] != -1:
                        gap = draw_idx - main_last_seen[num]
                        main_gaps[num].append(gap)
                    main_last_seen[num] = draw_idx
            
            # Process lucky stars
            drawn_lucky = [row[col] for col in self.lucky_stars]
            for num in range(1, 13):
                if num in drawn_lucky:
                    if lucky_last_seen[num] != -1:
                        gap = draw_idx - lucky_last_seen[num]
                        lucky_gaps[num].append(gap)
                    lucky_last_seen[num] = draw_idx
        
        # Current gaps (numbers that haven't appeared recently)
        current_draw = len(self.df) - 1
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
        
        for _, row in self.df.iterrows():
            main_nums = sorted([row[col] for col in self.main_balls])
            
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
        
        total_draws = len(self.df)
        print(f"Pattern frequencies out of {total_draws} draws:")
        print(f"  Consecutive pairs: {patterns['consecutive_pairs']} ({patterns['consecutive_pairs']/total_draws*100:.1f}%)")
        print(f"  Consecutive triplets: {patterns['consecutive_triplets']} ({patterns['consecutive_triplets']/total_draws*100:.1f}%)")
        print(f"  Same decade concentration: {patterns['same_decade']} ({patterns['same_decade']/total_draws*100:.1f}%)")
        print(f"  All odd: {patterns['all_odd']} ({patterns['all_odd']/total_draws*100:.1f}%)")
        print(f"  All even: {patterns['all_even']} ({patterns['all_even']/total_draws*100:.1f}%)")
        print(f"  Majority odd: {patterns['majority_odd']} ({patterns['majority_odd']/total_draws*100:.1f}%)")
        print(f"  Majority even: {patterns['majority_even']} ({patterns['majority_even']/total_draws*100:.1f}%)")
        
        print("\nSum ranges:")
        for sum_range, count in sorted(patterns['sum_ranges'].items()):
            print(f"  {sum_range}: {count} ({count/total_draws*100:.1f}%)")
        
        return patterns
    
    def hot_cold_analysis(self, recent_draws=50):
        """Analyze hot and cold numbers based on recent draws."""
        print(f"\n" + "="*50)
        print(f"HOT/COLD ANALYSIS (Last {recent_draws} draws)")
        print("="*50)
        
        recent_data = self.df.tail(recent_draws)
        
        # Recent frequency for main balls
        recent_main_balls = []
        for col in self.main_balls:
            recent_main_balls.extend(recent_data[col].tolist())
        
        recent_main_freq = Counter(recent_main_balls)
        
        print("HOT main balls (most frequent in recent draws):")
        for num, count in recent_main_freq.most_common(10):
            percentage = (count / len(recent_main_balls)) * 100
            print(f"  {num:2d}: {count:2d} times ({percentage:.1f}%)")
        
        print("\nCOLD main balls (least frequent in recent draws):")
        cold_main = [num for num in range(1, 51) if num not in recent_main_freq]
        if cold_main:
            print(f"  Numbers not drawn: {cold_main}")
        
        least_frequent_main = recent_main_freq.most_common()[-10:]
        for num, count in least_frequent_main:
            percentage = (count / len(recent_main_balls)) * 100
            print(f"  {num:2d}: {count:2d} times ({percentage:.1f}%)")
        
        # Recent frequency for lucky stars
        recent_lucky_stars = []
        for col in self.lucky_stars:
            recent_lucky_stars.extend(recent_data[col].tolist())
        
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
        most_frequent_lucky = [num for num, _ in lucky_freq.most_common(4)]
        predictions['most_frequent'] = {
            'main': np.random.choice(most_frequent_main, 5, replace=False).tolist(),
            'lucky': np.random.choice(most_frequent_lucky, 2, replace=False).tolist()
        }
        
        # Method 2: Overdue numbers (longest gaps)
        overdue_main = sorted(main_gaps.items(), key=lambda x: x[1], reverse=True)[:10]
        overdue_lucky = sorted(lucky_gaps.items(), key=lambda x: x[1], reverse=True)[:4]
        predictions['overdue'] = {
            'main': np.random.choice([num for num, _ in overdue_main], 5, replace=False).tolist(),
            'lucky': np.random.choice([num for num, _ in overdue_lucky], 2, replace=False).tolist()
        }
        
        # Method 3: Hot numbers (recent frequency)
        hot_main = [num for num, _ in recent_main_freq.most_common(10)]
        hot_lucky = [num for num, _ in recent_lucky_freq.most_common(4)]
        predictions['hot'] = {
            'main': np.random.choice(hot_main, 5, replace=False).tolist(),
            'lucky': np.random.choice(hot_lucky, 2, replace=False).tolist()
        }
        
        # Method 4: Balanced approach (mix of frequent and overdue)
        balanced_main_candidates = list(set(most_frequent_main[:7] + [num for num, _ in overdue_main[:7]]))
        balanced_lucky_candidates = list(set(most_frequent_lucky[:3] + [num for num, _ in overdue_lucky[:3]]))
        predictions['balanced'] = {
            'main': sorted(np.random.choice(balanced_main_candidates, 5, replace=False).tolist()),
            'lucky': sorted(np.random.choice(balanced_lucky_candidates, 2, replace=False).tolist())
        }
        
        # Method 5: Pattern-based prediction
        # Aim for typical patterns: mix of odd/even, reasonable sum, avoid all consecutive
        pattern_main = []
        while len(pattern_main) < 5:
            candidate = np.random.randint(1, 51)
            if candidate not in pattern_main:
                pattern_main.append(candidate)
        
        # Ensure mix of odd/even
        odd_count = sum(1 for num in pattern_main if num % 2 == 1)
        if odd_count < 2:  # Add more odds
            for i, num in enumerate(pattern_main):
                if num % 2 == 0 and odd_count < 3:
                    new_odd = np.random.choice([n for n in range(1, 51, 2) if n not in pattern_main])
                    pattern_main[i] = new_odd
                    odd_count += 1
        elif odd_count > 3:  # Add more evens
            for i, num in enumerate(pattern_main):
                if num % 2 == 1 and odd_count > 3:
                    new_even = np.random.choice([n for n in range(2, 51, 2) if n not in pattern_main])
                    pattern_main[i] = new_even
                    odd_count -= 1
        
        pattern_lucky = sorted(np.random.choice(range(1, 13), 2, replace=False).tolist())
        predictions['pattern_based'] = {
            'main': sorted(pattern_main),
            'lucky': pattern_lucky
        }
        
        # Method 6: AI/ML inspired (using weighted probabilities)
        main_weights = np.array([main_freq.get(i, 0) for i in range(1, 51)])
        gap_weights = np.array([1.0 / (main_gaps.get(i, 1) + 1) for i in range(1, 51)])
        combined_weights = main_weights * 0.7 + gap_weights * 0.3
        combined_weights = combined_weights / combined_weights.sum()
        
        ml_main = np.random.choice(range(1, 51), 5, replace=False, p=combined_weights).tolist()
        
        lucky_weights = np.array([lucky_freq.get(i, 0) for i in range(1, 13)])
        lucky_gap_weights = np.array([1.0 / (lucky_gaps.get(i, 1) + 1) for i in range(1, 13)])
        lucky_combined_weights = lucky_weights * 0.7 + lucky_gap_weights * 0.3
        lucky_combined_weights = lucky_combined_weights / lucky_combined_weights.sum()
        
        ml_lucky = np.random.choice(range(1, 13), 2, replace=False, p=lucky_combined_weights).tolist()
        
        predictions['ml_weighted'] = {
            'main': sorted(ml_main),
            'lucky': sorted(ml_lucky)
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
    
    def save_analysis_report(self, filename="lottery_analysis_report.txt"):
        """Save a comprehensive analysis report."""
        import sys
        from io import StringIO
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Run all analyses
            self.basic_statistics()
            self.gap_analysis()
            self.pattern_analysis()
            self.hot_cold_analysis()
            predictions = self.generate_predictions()
            
            # Get the captured output
            report_content = captured_output.getvalue()
            
        finally:
            # Restore stdout
            sys.stdout = old_stdout
        
        # Save to file
        with open(filename, 'w') as f:
            f.write(f"Euro Millions Lottery Analysis Report\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data: {len(self.df)} draws from {self.df['Date'].min()} to {self.df['Date'].max()}\n")
            f.write("=" * 80 + "\n\n")
            f.write(report_content)
        
        print(f"\n📊 Analysis report saved to: {filename}")
        return predictions

def main():
    """Main function to run the lottery analyzer."""
    print("🎰 Euro Millions Lottery Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = EuroMillionsAnalyzer('/Users/elbandi/Desktop/lotteryNumbers/lottery_results.csv')
    
    # Run comprehensive analysis
    predictions = analyzer.save_analysis_report('/Users/elbandi/Desktop/lotteryNumbers/analysis_report.txt')
    
    print("\n🎯 RECOMMENDED NEXT DRAW PREDICTIONS:")
    print("=" * 70)
    print("Based on comprehensive analysis, here are the top recommendations:")
    print()
    
    # Show balanced and ML predictions as top choices
    balanced = predictions['balanced']
    ml_weighted = predictions['ml_weighted']
    
    print("🥇 PRIMARY RECOMMENDATION (Balanced Method):")
    main_str = ' - '.join(f"{num:2d}" for num in balanced['main'])
    lucky_str = ' - '.join(f"{num:2d}" for num in balanced['lucky'])
    print(f"   Main Balls: {main_str}")
    print(f"   Lucky Stars: {lucky_str}")
    
    print("\n🥈 SECONDARY RECOMMENDATION (ML Weighted):")
    main_str = ' - '.join(f"{num:2d}" for num in ml_weighted['main'])
    lucky_str = ' - '.join(f"{num:2d}" for num in ml_weighted['lucky'])
    print(f"   Main Balls: {main_str}")
    print(f"   Lucky Stars: {lucky_str}")
    
    print("\n📈 Analysis complete! Check the full report for detailed insights.")

if __name__ == "__main__":
    main()
