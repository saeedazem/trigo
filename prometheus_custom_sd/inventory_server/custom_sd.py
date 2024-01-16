import requests
import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    # get sensor data
    response_data = requests.get('http://inventory-service:1337/inventory')
    sensor_data = response_data.json() if response_data.status_code == 200 else []

    # Convert sensor data to Prometheus exposition format
    metrics = []
    for sensor in sensor_data:
        value = random.randint(1, 100)
        metric = f'sensor_value{{sensor="{sensor}"}} {value}'
        metrics.append(metric)

    # Join metrics with newline characters
    response = "\n".join(metrics)

    return response, 200, {'Content-Type': 'text/plain; version=0.0.4'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
