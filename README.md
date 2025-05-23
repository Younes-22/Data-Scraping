Premier League 2023-2024 Data Scraping Project
Project Overview
This project extracts comprehensive statistics from the 2023-2024 Premier League season using advanced web scraping techniques. The data is collected from FBRef.com, a leading source of football statistics, and organized into structured CSV files for analysis. The project successfully navigates modern web protection mechanisms like Cloudflare to reliably gather player and team performance metrics.
Features

Complete Premier League Coverage: Extracts data for all 20 teams and their players from the 2023-2024 season
Multiple Statistical Categories: Collects standard player statistics along with specialized metrics (shooting, passing, defending, etc.)
Anti-Detection Mechanisms: Implements sophisticated techniques to bypass Cloudflare protection and avoid scraping detection
Robust Data Processing: Handles complex table structures, multi-level columns, and inconsistent formatting
Comprehensive Data Cleaning: Converts data to appropriate types, handles missing values, and standardizes formats
Data Analysis & Visualization: Includes scripts for analyzing the collected data and generating insightful visualizations

Technologies Used

Selenium: Controls a Chrome browser to access JavaScript-rendered content and bypass Cloudflare protection
BeautifulSoup: Parses HTML content and isolates the required data elements
Pandas: Processes tabular data, handles data transformation, and exports to CSV files
Chrome WebDriver: Enables browser automation through Selenium
Matplotlib/Seaborn: Creates visualizations of player and team statistics (in analysis scripts)