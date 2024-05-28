import os
import faust

from database import MongoDB
from models import ScrapedNews


KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9092')
MONGODB_CONNECTION_STRING = 'mongodb://172.31.62.156:27017/'

app = faust.App('myapp', broker=KAFKA_BROKER_URL)
scraped_news_topic = app.topic('scraping', value_type=ScrapedNews)

# create a MongoDB instance (for saving the data after processing)
mongodb = MongoDB('news_articles', 'scraped_data', MONGODB_CONNECTION_STRING)

from pymongo.errors import PyMongoError

@app.agent(scraped_news_topic)
async def save_raw_news(scraped_news):
    async for news in scraped_news:
        # Convert the news object to a dictionary
        news_dict = news.asdict()

        # Use the URL as the key (_id) for the MongoDB document
        news_dict['_id'] = news_dict['article_url']

        try:
            # name = mongodb.get_database_list()
            # print("Connected to MongoDB.")
            # print(name)


            # Check if the document already exists
            if mongodb.collection.find_one({'_id': news_dict['_id']}):
                print(f"Document with _id {news_dict['_id']} already exists. Skipping.")
                continue

            # Save the data to MongoDB
            mongodb.collection.insert_one(news_dict)
            print(f"Saved news with _id {news_dict['_id']} to MongoDB.")
        except PyMongoError as e:
            print(f"An error occurred while saving the news to MongoDB: {e}")


if __name__ == '__main__':
    app.main()
