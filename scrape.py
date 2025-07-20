from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

# Define a basic proxy if needed. This will NOT handle authentication.
# For example, a free public HTTP proxy (use with caution and for testing only)
# BASIC_PROXY_ADDRESS = os.getenv('BASIC_PROXY_ADDRESS', 'http://YOUR_BASIC_PROXY_IP:PORT')
# If you don't need a proxy, you can set this to an empty string or None.
BASIC_PROXY_ADDRESS = "" # Set to your basic proxy address, e.g., 'http://1.2.3.4:8080'

def scrape_website(website):
    """
    Scrapes the content of a given website using basic Selenium.
    No selenium-wire, no authenticated proxy, no explicit CAPTCHA solving.
    """
    print("Launching chrome browser ...")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless') # Run in headless mode for server environments
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Add basic proxy argument if BASIC_PROXY_ADDRESS is set
    if BASIC_PROXY_ADDRESS:
        chrome_options.add_argument(f'--proxy-server={BASIC_PROXY_ADDRESS}')
        print(f"Using basic proxy: {BASIC_PROXY_ADDRESS}")
    else:
        print("Not using any proxy.")

    service = Service(ChromeDriverManager().install())
    driver = None # Initialize driver to None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(website)
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None
    finally:
        if driver:
            driver.quit() # Ensure the browser is closed

def extract_body_content(html_content):
    """
    Extracts the content within the <body> tags of an HTML string.
    """
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body

    if body_content:
        return str(body_content)

    return ""

def clean_body_content(body_content):
    """
    Cleans the body content by removing script/style tags and excess whitespace.
    """
    if not body_content:
        return ""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    # Get text and clean up lines
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """
    Splits a long string of DOM content into smaller chunks.
    """
    if not dom_content:
        return [""]
    return [dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)]
