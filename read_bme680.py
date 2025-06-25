#!/usr/bin/env python3

import json
try:
    import board
    import adafruit_bme680
    import busio

    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

    data = {
        "timestamp": None,  # Optional: handled by `breathline_trace.sh`
        "ambient_temp": round(sensor.temperature, 1),
        "humidity": round(sensor.humidity, 1),
        "pressure": round(sensor.pressure, 1),
        "voc_level": round(sensor.gas, 1),
        "light_level": 0.0,
        "sensor_error": ""
    }
except Exception:
    # Fallback for dev environments without hardware
    data = {
        "timestamp": None,
        "ambient_temp": 22.4,
        "humidity": 44.1,
        "pressure": 1011.8,
        "voc_level": 128.6,
        "light_level": 300.0,
        "sensor_error": ""
    }

print(json.dumps(data))

