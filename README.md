# CyberSense V1

CyberSense V1 is an automated tool for aggregating, filtering, and exporting cybersecurity news and vulnerability advisories from multiple RSS feeds. It is designed to help security professionals, researchers, and organizations stay up-to-date with the latest threats and advisories relevant to their products and interests.

## Features

- **Aggregates news** from multiple security-focused RSS feeds
- **Keyword-based filtering** for products, vendors, and vulnerability terms
- **Customizable time window** for news collection
- **Cleans and normalizes** news content for easy reading
- **Exports results** to CSV for further analysis or reporting
- **Command-line interface** with interactive prompts
- **ASCII art banner and author info** for branding

## Usage

1. **Install dependencies:**
   ```bash
   pip install feedparser pandas tqdm beautifulsoup4
   ```

2. **Run the script:**
   ```bash
   python news_automate.py
   ```

3. **Follow the prompts:**
   - Select products/keywords to filter news
   - Choose how many days back to fetch news
   - The filtered news will be saved as a CSV file in the current directory

## Configuration
- You can add or remove RSS feeds in the `rss_feeds` list in `news_automate.py`.
- You can customize product keywords in the `product_keywords` list.

## Example Output
A CSV file named like `vulnerability_news_20250523.csv` containing columns:
- Title
- Description
- Link
- Published Date
- severity

  

## Author
Jeyaradnam Tharjalan - 0xtmax

## License
This project is licensed for demonstration and educational purposes. For commercial use, please contact the author.
www.linkedin.com/in/tharjalan-jeyaradnam-345103145
---

*CyberSense V1 helps you stay ahead of the latest cybersecurity threats!*
