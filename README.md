# EuroMillions Lottery Analysis 🎰

An advanced statistical analysis system for EuroMillions lottery data.


## Features

- **Comprehensive Analysis**: Analyses 20+ years of EuroMillions data (2004-2025)
- **Multiple Prediction Methods**: 6 different statistical approaches
- **Automated Reports**: GitHub Actions automatically generates analysis reports
- **Web Interface**: Beautiful HTML reports deployed to GitHub Pages
- **Real-time Updates**: Analysis runs automatically on every push to the main branch

## Analysis Methods

1. **Most Frequent**: Based on historical frequency
2. **Overdue Numbers**: Focuses on numbers with longest gaps
3. **Hot Numbers**: Recent high-frequency trends
4. **Balanced Approach**: Combines frequent + overdue strategies
5. **Pattern-Based**: Ensures realistic number distributions
6. **Weighted Random**: Statistical probability-based selection

## GitHub Pages 

Results: [here](https://elasbandis.github.io/lucky-draft/)

## Local Development

### Prerequisites
- Python 3.8+
- PHP 7.4+ (for data extraction)

### Installation
```bash
pip install pandas numpy matplotlib seaborn
```

### Running Analysis Locally
```bash
# Generate CSV from HTML data
php csvGen.php

# Run analysis
python3 lottery_analyzer_simple.py

# Generate HTML report
python3 generate_html_report.py
```

## File Structure

```
├── .github/workflows/
│   └── lottery-analysis.yml    # GitHub Actions workflow
├── results/                    # HTML data files by year from https://www.euro-millions.com/
│   ├── 2004.html
│   ├── 2005.html
│   └── ...
├── csvGen.php                  # PHP data extraction script
├── lottery_analyzer_simple.py  # Main analysis script
├── generate_html_report.py     # HTML report generator
├── lottery_results.csv         # Processed lottery data
└── docs/                       # Generated GitHub Pages content
    └── index.html
```

## Data Sources

- **Historical Data**: EuroMillions draws from 2004-2025
- **Data Format**: CSV with Date, 5 Main Balls (1-50), 2 Lucky Stars (1-12)
- **Update Frequency**: Manual HTML file updates, automatic analysis

## Analysis Output

The system provides:
- **Frequency Analysis**: Most/least common numbers
- **Gap Analysis**: Overdue numbers
- **Pattern Analysis**: Consecutive pairs, odd/even distributions
- **Hot/Cold Analysis**: Recent performance trends
- **Multiple Predictions**: 6 different methodological approaches

## Predictions Disclaimer

⚠️ **Important**: This analysis is for educational and entertainment purposes only. Lottery results are random, and past performance does not predict future outcomes. Please gamble responsibly.
 
## Customisation

### Modify Analysis Parameters
Edit `lottery_analyzer_simple.py` to adjust:
- Recent draws window (default: 50)
- Prediction methods
- Statistical weights

### Styling Changes
Modify `generate_html_report.py` to customise:
- CSS styling
- Report layout
- Additional statistics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is open source and available under the MIT License.
