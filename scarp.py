import requests
from bs4 import BeautifulSoup
import schedule
import time

def scrape_articles(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')  # Assuming articles are wrapped in <article> tags
            article_titles = [article.find('h2').text.strip() for article in articles]
            return article_titles
        else:
            print("Failed to fetch webpage. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def fetch_and_print_updates(url):
    print("Fetching articles from", url, "at", time.strftime("%Y-%m-%d %H:%M:%S"))
    article_titles = scrape_articles(url)
    
    if article_titles:
        print("Article titles:")
        for title in article_titles:
            print("- ", title)
    else:
        print("No articles scraped.")

if __name__ == "__main__":
    url = input("Enter the URL of the website to scrape: ")
    
    # Initial scraping
    fetch_and_print_updates(url)
    
    # Schedule scraping every hour
    schedule.every().hour.do(fetch_and_print_updates, url)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
