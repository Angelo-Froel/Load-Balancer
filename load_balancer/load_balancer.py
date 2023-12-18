from flask import Flask, request, jsonify
import time
import requests
import sys

app = Flask(__name__)

# Maintain a dictionary to store device IDs and their corresponding ports
device_ports_mapping = {
    "device1": 6001,
    "device2": 6002,
    "device3": 6003
}

def send_server(data, time_receive_lb):
    server_url = "http://server:5001/receive"
    payload = {
        "packet_id": data.get("packet_id"),
        "time_sent_dev": data.get("time_sent_dev"),
        "device_id": data.get("device_id"),
        "time_sent_lb": time.time(),
        "time_receive_lb": time_receive_lb
    }

    # Get the device port from the headers
    device_port = request.headers.get("Device-Port")

    # Use the device_ports_mapping dictionary to get the actual port for the device
    actual_device_port = device_ports_mapping.get(f"device{data['device_id']}")

    # Build the device URL with the obtained actual device port
    device_url = f"http://device{data['device_id']}:{actual_device_port}/receive"

    # Set the actual device port in the headers for the server
    headers = {"Device-Port": str(actual_device_port)}

    try:
        response = requests.post(device_url, json=payload, headers=headers)
        packet_id = payload.get("packet_id")
        print(f"Load balancer -> Server | Packet: {packet_id}")
        sys.stdout.flush()
        return jsonify(success=True)
    except Exception as e:
        print(f"Error sending packet to server: {e}")
        sys.stdout.flush()
        return jsonify(error=str(e)), 500

@app.route('/receive', methods=['POST'])
def receive_packets():
    data = request.json
    time_receive_lb = time.time()
    response = send_server(data, time_receive_lb)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
