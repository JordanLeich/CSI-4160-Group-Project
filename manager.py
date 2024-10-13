from flask import Flask, render_template, jsonify
import psutil
from sense_hat import SenseHat
import time

app = Flask(__name__)
sense = SenseHat()

# Serve the index page for the game
@app.route('/')
def index():
    return render_template('index.html')

# Serve the system monitor page
@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

# Monitor resources: CPU, RAM, and Storage
@app.route('/monitor_resources', methods=['GET'])
def monitor_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = {
        "total": memory_info.total,
        "used": memory_info.used,
        "free": memory_info.free,
        "percent": memory_info.percent
    }
    disk_info = psutil.disk_usage('/')
    disk_usage = {
        "total": disk_info.total,
        "used": disk_info.used,
        "free": disk_info.free,
        "percent": disk_info.percent
    }

    resource_info = {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }

    return jsonify(resource_info)

# Monitor Sense HAT sensors: Temperature, Humidity, and Pressure
@app.route('/monitor_sensors', methods=['GET'])
def monitor_sensors():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()

    sensor_data = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure
    }

    return jsonify(sensor_data)

# System uptime monitoring
@app.route('/uptime', methods=['GET'])
def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    uptime_info = {
        "uptime_seconds": uptime_seconds,
        "uptime_hours": uptime_seconds / 3600
    }
    return jsonify(uptime_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
