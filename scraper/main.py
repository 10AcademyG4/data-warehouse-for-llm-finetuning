from news_scrapper import NewsScraper
import pprint
import time
from kafka.errors import NoBrokersAvailable

def hello():
    url = 'https://am.al-ain.com/'
    pages_to_scrape = 1
    MAX_RETRIES = 5
    RETRY_DELAY = 2  # delay between retries in seconds

    while True:
        for i in range(MAX_RETRIES):
            try:
                print("Scraping started ")

                scraper = NewsScraper(url, pages_to_scrape)
                # If the initialization is successful, break from the loop
                break
            except NoBrokersAvailable as e:
                print(f"An error occurred: {e}")
                if i < MAX_RETRIES - 1:  # No need to sleep on the last iteration
                    time.sleep(RETRY_DELAY)
                else:
                    raise  # Re-raise the last exception if all retries failed
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                raise

        news = scraper.scrape_news()

        pages_to_scrape += 1

        # for article in news:
        #     pprint.pprint(article)

if __name__ == "__main__":
    hello()