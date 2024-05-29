from confluent_kafka import Consumer, KafkaException

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

def create_consumer():
  consumer = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,  # replace with your Kafka bootstrap servers
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
  })

  consumer.subscribe(['scraped_news_data'])  # replace with your topic name

  try:
    while True:
      msg = consumer.poll(1.0)

      if msg is None:
        continue
      if msg.error():
        raise KafkaException(msg.error())
      else:
        print('Received message: {}'.format(msg.value().decode('utf-8')))

  except KeyboardInterrupt:
    pass
  finally:
    consumer.close()

if __name__ == '__main__':
  create_consumer()