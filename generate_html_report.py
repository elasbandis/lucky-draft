#!/usr/bin/env python3
"""
Generate HTML report from lottery analysis output
"""

import os
import subprocess
import sys
from datetime import datetime
import csv

def run_analysis():
    """Run the lottery analyzer and capture output"""
    try:
        # Run the analyzer and capture output
        result = subprocess.run(['python3', 'lottery_analyzer_simple.py'], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running analysis: {e}")
        return f"Error running analysis: {e.stderr}"

def load_latest_predictions():
    """Load latest predictions from CSV if available"""
    try:
        with open('lottery_results.csv', 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
            latest_draw = data[-1] if data else None
            return latest_draw, len(data)
    except FileNotFoundError:
        return None, 0

def generate_html_report(analysis_output):
    """Generate HTML report with analysis results"""
    
    latest_draw, total_draws = load_latest_predictions()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Create docs directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EuroMillions Lottery Analysis</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2a5298;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .analysis-output {{
            padding: 30px;
            background: white;
        }}
        
        .analysis-output h2 {{
            color: #2a5298;
            border-bottom: 3px solid #2a5298;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        
        .output-content {{
            background: #1a1a1a;
            color: #00ff00;
            padding: 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            white-space: pre-wrap;
            line-height: 1.4;
        }}
        
        .predictions-section {{
            background: #f8f9fa;
            padding: 30px;
        }}
        
        .prediction-card {{
            background: white;
            margin: 15px 0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .ball {{
            display: inline-block;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #2a5298;
            color: white;
            text-align: center;
            line-height: 40px;
            margin: 5px;
            font-weight: bold;
        }}
        
        .lucky-star {{
            background: #ffd700;
            color: #333;
        }}
        
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        
        .update-time {{
            background: #e9ecef;
            padding: 15px;
            text-align: center;
            color: #666;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            body {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎰 EuroMillions Lottery Analysis</h1>
            <div class="subtitle">Advanced Statistical Analysis & Predictions</div>
        </div>
        
        <div class="update-time">
            Last Updated: {current_time}
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_draws:,}</div>
                <div class="stat-label">Total Draws Analyzed</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">21</div>
                <div class="stat-label">Years of Data</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">6</div>
                <div class="stat-label">Prediction Methods</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">50</div>
                <div class="stat-label">Main Ball Range</div>
            </div>
        </div>
"""

    # Add latest draw info if available
    if latest_draw:
        html_content += f"""
        <div class="predictions-section">
            <h2>📊 Latest Draw Information</h2>
            <div class="prediction-card">
                <h3>Most Recent Draw: {latest_draw[0]}</h3>
                <div>
                    Main Balls: 
                    <span class="ball">{latest_draw[1]}</span>
                    <span class="ball">{latest_draw[2]}</span>
                    <span class="ball">{latest_draw[3]}</span>
                    <span class="ball">{latest_draw[4]}</span>
                    <span class="ball">{latest_draw[5]}</span>
                </div>
                <div style="margin-top: 10px;">
                    Lucky Stars: 
                    <span class="ball lucky-star">{latest_draw[6]}</span>
                    <span class="ball lucky-star">{latest_draw[7]}</span>
                </div>
            </div>
        </div>
"""

    html_content += f"""
        <div class="analysis-output">
            <h2>🔍 Complete Analysis Output</h2>
            <div class="output-content">{analysis_output}</div>
        </div>
        
        <div class="footer">
            <p>🎯 EuroMillions Lottery Analysis System | Generated automatically via GitHub Actions</p>
            <p>⚠️ Disclaimer: This analysis is for educational purposes only. Lottery results are random and past performance does not guarantee future results.</p>
        </div>
    </div>
</body>
</html>"""
    
    # Write HTML file
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML report generated successfully!")
    print("📄 Report saved to: docs/index.html")

def main():
    """Main function"""
    print("🎰 Generating EuroMillions Lottery Analysis Report...")
    
    # Run analysis
    print("📊 Running lottery analysis...")
    analysis_output = run_analysis()
    
    # Generate HTML report
    print("🌐 Generating HTML report...")
    generate_html_report(analysis_output)
    
    print("✨ Report generation complete!")

if __name__ == "__main__":
    main()
