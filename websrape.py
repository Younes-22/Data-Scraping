from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Path to your ChromeDriver
webdriver_path = './chromedriver.exe'

# Setup Selenium
options = webdriver.ChromeOptions()
# Add options to make browser less detectable
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Modify the user agent
driver.execute_cdp_cmd("Network.setUserAgentOverride", {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
})

# Set a 30 second wait for elements to load
wait = WebDriverWait(driver, 30)

# Function to wait for page to load and handle Cloudflare
def load_page(url):
    driver.get(url)
    # Wait for the page to load
    time.sleep(5)
    # Check if Cloudflare challenge is present
    try:
        # If there's a Cloudflare challenge, wait longer for it to resolve
        if "Checking your browser" in driver.page_source or "Just a moment" in driver.page_source:
            print("Cloudflare detected - waiting...")
            time.sleep(10)  # Wait longer to pass the challenge
    except:
        pass

all_teams = []  # List to store all teams

# Load the main stats page for 2023-2024 season
season_url = 'https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats'
load_page(season_url)

# Get the HTML content after JavaScript has loaded
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'lxml')

# Find the main table
try:
    table = soup.find_all('table', class_='stats_table')[0]  # First table
    links = table.find_all('a')
    links = [l.get("href") for l in links]
    links = [l for l in links if '/squads/' in l]  # Filter for squad links
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    print(f"Found {len(team_urls)} team URLs")
    
    # Iterate through each team
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        print(f"Processing team: {team_name}")
        
        # Load the team page
        load_page(team_url)
        team_html = driver.page_source
        team_soup = BeautifulSoup(team_html, 'lxml')
        
        try:
            # Find the stats table
            stats_tables = team_soup.find_all('table', class_="stats_table")
            if stats_tables:
                stats = stats_tables[0]  # First table with player stats
                
                # Convert to DataFrame
                team_dfs = pd.read_html(str(stats))
                if team_dfs:
                    team_data = team_dfs[0]
                    # Drop multi-level columns if present
                    if isinstance(team_data.columns, pd.MultiIndex):
                        team_data.columns = team_data.columns.droplevel()
                    
                    # Add team name column
                    team_data["Team"] = team_name
                    all_teams.append(team_data)
                    print(f"Added data for {team_name}, shape: {team_data.shape}")
                else:
                    print(f"No data found for {team_name}")
            else:
                print(f"No stats table found for {team_name}")
        except Exception as e:
            print(f"Error processing {team_name}: {str(e)}")
        
        # Delay to avoid being detected as a bot
        time.sleep(7)  # Random delay between 5-10 seconds
        
except Exception as e:
    print(f"Error with main page: {str(e)}")

# Clean up and save data
if all_teams:
    try:
        stat_df = pd.concat(all_teams, ignore_index=True)
        # Save to CSV
        csv_path = "premier_league_stats_23_24.csv"
        stat_df.to_csv(csv_path, index=False)
        print(f"Data saved to {csv_path}. Total rows: {len(stat_df)}")
    except Exception as e:
        print(f"Error saving data: {str(e)}")
else:
    print("No team data collected")

# Don't forget to close the driver
driver.quit()