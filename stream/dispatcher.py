"""Publishes a food/ride request every 2 s to the topic exchange 'rapido-dispatch'.
   python stream/dispatcher.py [--bad-every 10]   (0 = never send a bad message)"""
import argparse, json, os, random, time, uuid
import pika

CITIES = {"bangalore": ["koramangala", "indiranagar", "whitefield"],
          "chennai": ["tnagar", "adyar", "whitefield"]}

ap = argparse.ArgumentParser()
ap.add_argument("--bad-every", type=int, default=10)
args = ap.parse_args()

conn = pika.BlockingConnection(pika.URLParameters(os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/%2F")))
ch = conn.channel()
ch.exchange_declare(exchange="rapido-dispatch", exchange_type="topic")

n = 0
try:
    while True:
        n += 1
        city = random.choice(list(CITIES)); zone = random.choice(CITIES[city]); typ = random.choice(["ride", "food"])
        msg = {"id": str(uuid.uuid4())[:8], "city": city, "zone": zone, "type": typ, "ts": time.time()}
        if args.bad_every and n % args.bad_every == 0:
            del msg["zone"]                                  # D3: a bad message
        key = f"{city}.{zone}.{typ}"
        ch.basic_publish(exchange="rapido-dispatch", routing_key=key, body=json.dumps(msg))
        print(f"#{n} published key={key} {'(BAD: no zone)' if 'zone' not in msg else ''}", flush=True)
        time.sleep(2)
except KeyboardInterrupt:
    conn.close()
