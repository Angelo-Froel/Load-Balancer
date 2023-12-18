from flask import Flask, request, jsonify
import time
import sys

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive_packets():
    data = request.json
    packet_id = data.get("packet_id")
    time_sent_dev = data.get("time_sent_dev")
    device_id = data.get("device_id")
    time_sent_lb = data.get("time_sent_lb")
    time_receive_lb = data.get("time_receive_lb")

    print(f"Server <- Load balancer | Packet: {packet_id} | Device: {device_id}")
    sys.stdout.flush()

    # Simulate some processing time
    time.sleep(1)

    # Send the packet back to the device
    return jsonify({
        "packet_id": packet_id,
        "time_sent_dev": time_sent_dev,
        "device_id": device_id,
        "time_sent_lb": time_sent_lb,
        "time_receive_lb": time_receive_lb,
        "time_received_server": time.time()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
