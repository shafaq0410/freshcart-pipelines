
import json
import os
import time
import pika

OUTPUT_FILE = "streamed_orders.json"
COLLECTION_SECONDS = 60

url = os.getenv(
    "AMQP_URL",
    "amqp://guest:guest@localhost:5672/%2F"
)

connection = pika.BlockingConnection(pika.URLParameters(url))
channel = connection.channel()

channel.exchange_declare(
    exchange="freshcart-orders",
    exchange_type="topic",
    durable=True
)

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange="freshcart-orders",
    queue=queue_name,
    routing_key="freshcart.orders"
)

orders = []

def on_message(ch, method, properties, body):
    try:
        order = json.loads(body)
        orders.append(order)
        print(f"Received: {order['order_id']}", flush=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as error:
        print(f"Rejected message: {error}", flush=True)
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )

channel.basic_consume(
    queue=queue_name,
    on_message_callback=on_message,
    auto_ack=False
)

print("Collecting FreshCart orders for 60 seconds...")

start = time.monotonic()

try:
    while time.monotonic() - start < COLLECTION_SECONDS:
        connection.process_data_events(time_limit=1)
finally:
    channel.close()
    connection.close()

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(orders, file, indent=2)

print(f"Collection complete: {len(orders)} orders saved to {OUTPUT_FILE}")
