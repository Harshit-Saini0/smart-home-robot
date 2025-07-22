import Adafruit_DHT

# Sensor type and GPIO assignment
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 7              # GPIO7

# Try to grab a sensor reading. Use a loop to try multiple times if failed
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if humidity is not None and temperature is not None:
    print(f"Temp={temperature:0.1f}°C  Humidity={humidity:0.1f}%")
else:
    print("Failed to retrieve data from DHT22 sensor")
