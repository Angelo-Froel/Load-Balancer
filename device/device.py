import os
import sys
import requests
import time
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

device_id = os.environ.get("DEVICE_ID", "1")

packet_id = random.randint(1, 100)
payload = {
    "packet_id": packet_id,
    "time_sent_lb": time.time(),
    "device_id": device_id
}

load_balancer_url = "http://load_balancer:5000/receive"
response = requests.post(load_balancer_url, json=payload, headers={"Device-Port": os.environ.get("DEVICE_PORT", "5000")})

print(f"Device {device_id} -> Load balancer | Packet: {packet_id}")
sys.stdout.flush()
time.sleep(random.uniform(1, 5))


@app.route('/receive', methods=['POST'])
def receive_packets():
    data = request.json
    div_id = data["device_id"]
    pack_id = data["packet_id"]
    print(f"Packet received at device {div_id} | Packet: {pack_id}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("DEVICE_PORT", "5000")))
