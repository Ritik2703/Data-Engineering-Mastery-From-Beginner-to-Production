"""
Kafka streaming example — producer emits order events, consumer processes them in real time.
pip install kafka-python
"""

# ---------------- PRODUCER ----------------
from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",           # wait for all replicas to acknowledge (durability)
    retries=5,
)

def produce_order_events():
    for i in range(100):
        event = {
            "order_id": f"ORD{1000 + i}",
            "customer_id": random.randint(1, 500),
            "amount": round(random.uniform(10, 500), 2),
            "event_time": time.time(),
        }
        producer.send("orders_topic", value=event, key=str(event["customer_id"]).encode())
        time.sleep(0.1)
    producer.flush()


# ---------------- CONSUMER ----------------
from kafka import KafkaConsumer

def consume_order_events():
    consumer = KafkaConsumer(
        "orders_topic",
        bootstrap_servers=["localhost:9092"],
        group_id="order-processing-group",
        auto_offset_reset="earliest",   # start from beginning if no committed offset
        enable_auto_commit=False,       # manual commit for at-least-once processing
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )

    for message in consumer:
        event = message.value
        # ... business logic: write to DB, trigger alert, update running aggregate ...
        print(f"Processed order {event['order_id']} amount={event['amount']}")

        # Commit offset only after successful processing (avoids data loss on crash)
        consumer.commit()


if __name__ == "__main__":
    produce_order_events()
    # consume_order_events()  # run in a separate process/terminal
