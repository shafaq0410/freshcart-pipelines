"""python stream/driver.py NAME PATTERN     e.g.  python stream/driver.py Ravi 'bangalore.koramangala.*'"""
import json, os, sys
import pika

name, pattern = sys.argv[1], sys.argv[2]
conn = pika.BlockingConnection(pika.URLParameters(os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")))
ch = conn.channel()
ch.exchange_declare(exchange="rapido-dispatch", exchange_type="topic")
q = ch.queue_declare(queue="", exclusive=True).method.queue      # private, auto-named, deleted on disconnect
ch.queue_bind(exchange="rapido-dispatch", queue=q, routing_key=pattern)
ch.basic_qos(prefetch_count=1)


def on_message(ch, method, props, body):
    msg = json.loads(body)
    if "zone" not in msg:                                        # D3: reject bad messages, do not requeue
        print(f"[{name}] REJECT key={method.routing_key} {msg}", flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return
    print(f"[{name}] got key={method.routing_key} id={msg['id']}", flush=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)               # D2: ACK after processing


ch.basic_consume(queue=q, on_message_callback=on_message, auto_ack=False)
print(f"[{name}] bound '{pattern}' to {q}; waiting...", flush=True)
try:
    ch.start_consuming()
except KeyboardInterrupt:
    conn.close()
