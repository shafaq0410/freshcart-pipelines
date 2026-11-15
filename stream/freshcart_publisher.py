
import json
import os
import pika

orders = [
    {
        "order_id": "ORD-STREAM-001",
        "cust_email": "arjun.k@yahoo.in",
        "cust_name": "Arjun K",
        "order_date": "2026-09-01",
        "amount": "10.00",
        "currency": "USD",
        "pincode": "560034",
        "updated_at": "2026-09-01 10:00:00"
    },
    {
        "order_id": "ORD-STREAM-002",
        "cust_email": "arjun.k@yahoo.in",
        "cust_name": "Arjun K",
        "order_date": "2026-09-01",
        "amount": "20.00",
        "currency": "USD",
        "pincode": "560034",
        "updated_at": "2026-09-01 10:05:00"
    },
    {
        "order_id": "ORD-STREAM-003",
        "cust_email": "arjun.k@yahoo.in",
        "cust_name": "Arjun K",
        "order_date": "2026-09-01",
        "amount": "15.00",
        "currency": "USD",
        "pincode": "560034",
        "updated_at": "2026-09-01 10:10:00"
    }
]

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

for order in orders:
    channel.basic_publish(
        exchange="freshcart-orders",
        routing_key="freshcart.orders",
        body=json.dumps(order),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2
        )
    )
    print(f"Published: {order['order_id']}")

connection.close()
print("All 3 FreshCart orders published.")
