import feedparser
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import html
import re

ascii_banner = r"""
  _______           ___.                       _________                                        
 /  _____/  ___.__.\_ |__    ____  _______   /   _____/  ____    ____    ______  ____  
/   \  ___ <   |  | | __ \ _/ __ \ \_  __ \  \_____  \ _/ __ \  /    \  /  ___/_/ __ \  
\    \_\  \\___  | | \_\ \\  ___/  |  | \/  /        \\  ___/ |   |  \ \___ \ \  ___/   
 \______  // ____| |___  / \___  > |__|    /_______  / \___  >|___|  //____  > \___  >  
        \/ \/          \/      \/                  \/      \/      \/      \/      \/      
            
 CyberSense V1
Author: Jeyaradnam Tharjalan - 0xtmax
"""

# Define RSS feeds related to vulnerabilities and security advisories
rss_feeds = [
    #"https://cvefeed.io/rssfeed/severity/high.xml", #CVE Feed of High & Critical Severity
    #"https://cvefeed.io/rssfeed/latest.xml", #News Room feed
    "http://feeds.trendmicro.com/Anti-MalwareBlog/",
    "http://feeds.trendmicro.com/TrendMicroSimplySecurity",
    "http://thehackernews.com/feeds/posts/default",
    "http://www.bleepingcomputer.com/feed/",
    "http://researchcenter.paloaltonetworks.com/feed/",
    # Add more feeds as necessary
]

# Define product keywords related to vulnerabilities (tailored for specific products)
product_keywords = [
    "VMware", "Trend Micro", "Microsoft", "Linux", "Palo Alto", "Cisco",
    "Malwarebytes", "Krebs", "vulnerability", "CVE", "security advisory"
]

def select_products(keywords):
    print("Available products/keywords:")
    for idx, kw in enumerate(keywords, 1):
        print(f"{idx}. {kw}")
    selected = input("Enter numbers separated by commas (e.g., 1,3,5) or 'all': ")
    if selected.strip().lower() == 'all':
        return keywords
    indices = [int(i.strip())-1 for i in selected.split(",") if i.strip().isdigit()]
    return [keywords[i] for i in indices if 0 <= i < len(keywords)]

def get_start_date_auto():
    days = input("Fetch news from how many days ago? (default 1): ")
    try:
        days = int(days)
    except:
        days = 1
    return datetime.now() - timedelta(days=days)

def clean_html(content):
    if not isinstance(content, str):
        return ""
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text(separator=" ").strip()
    text = re.sub(r"\|\s*\d+\s*(hour|minute|minutes|day|hours)s?\,?\s*\d+\s*(hour|minute|minutes|day|hours)s? ago", "", text)
    return " ".join(text.split())

def fetch_filtered_vulnerability_news(feeds, keywords, start_date):
    news_items = []
    for feed_url in tqdm(feeds, desc="Fetching vulnerability feeds"):
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.get("title", "")
            description = entry.get("description", "") or entry.get("summary", "")
            link = entry.get("link", "")
            published_date = entry.get("published", "")
            try:
                published_datetime = datetime(*entry.published_parsed[:6])
            except Exception:
                published_datetime = None
            if published_datetime and published_datetime >= start_date:
                clean_description = clean_html(description)
                if any(keyword.lower() in (title + clean_description).lower() for keyword in keywords):
                    news_items.append({
                        "title": title,
                        "description": clean_description,
                        "link": link,
                        "published Date": published_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    })
    return news_items

if __name__ == "__main__":
    print(ascii_banner)
    selected_keywords = select_products(product_keywords)
    start_date = get_start_date_auto()
    filtered_news = fetch_filtered_vulnerability_news(rss_feeds, selected_keywords, start_date)
    if filtered_news:
        df = pd.DataFrame(filtered_news)
        output_file = f"vulnerability_news_{start_date.strftime('%Y%m%d')}.csv"
        with tqdm(total=1, desc="Saving news to CSV", ncols=100) as pbar:
            df.to_csv(output_file, index=False, encoding='utf-8')
            # Save a copy as latest_report.csv for the HTML dashboard
            df.to_csv("latest_report.csv", index=False, encoding='utf-8')
            pbar.update(1)
        print(f"Filtered vulnerability news successfully saved to {output_file} and latest_report.csv")
    else:
        print("No vulnerability-related news items matched the given keywords and date filter.")

    # Start a local HTTP server and print the link
    import os
    import sys
    import subprocess
    port = 8000
    print(f"\nStarting local server for dashboard...")
    print(f"Open http://localhost:{port}/index.html in your browser to view the report.")
    if sys.platform.startswith('win'):
        # Use powershell to start the server in a new window
        subprocess.Popen(["powershell", "-NoExit", "python", "-m", "http.server", str(port)], cwd=os.path.dirname(os.path.abspath(__file__)))
    else:
        subprocess.Popen([sys.executable, "-m", "http.server", str(port)], cwd=os.path.dirname(os.path.abspath(__file__)))