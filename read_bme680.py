import json
try:
    import board
    import adafruit_bme680
    import busio
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    data = {
        "temperature": round(sensor.temperature, 1),
        "humidity": round(sensor.humidity, 1),
        "pressure": round(sensor.pressure, 1),
        "gas": round(sensor.gas, 1),
        "light": 0.0
    }
except Exception:
    # Fallback for dev environments without hardware
    data = {
        "temperature": 22.4,
        "humidity": 44.1,
        "pressure": 1011.8,
        "gas": 128.6,
        "light": 300.0
    }

print(json.dumps(data))

