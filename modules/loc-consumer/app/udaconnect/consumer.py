import os
import logging
import json
import psycopg2
from kafka import KafkaConsumer

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

consumer = KafkaConsumer(
    "Locations",
    bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092",
)

def save_location(location):
    connection = psycopg2.connect(
        dbname=DB_NAME,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
    )
    query = "INSERT INTO location (person_id, coordinate) VALUES ({}, ST_Point({}, {}));".format(
        int(location["person_id"]),
        float(location["latitude"]),
        float(location["longitude"]),
    )

    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def consume():
    for message in consumer:
        print("Location received: {}".format(message))

        decoded_message = message.value.decode("utf-8")
        location = json.loads(decoded_message)

        save_location(location)

if __name__ == "__main__":
    logging.basicConfig()
    while True:
        consume()