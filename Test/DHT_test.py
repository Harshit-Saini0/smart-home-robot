import time
import board
import adafruit_dht

# Set up DHT22 sensor on GPIO board

sensor = adafruit_dht.DHT22(board.D7)

while True:
    try:
        temperature = (sensor.temperature) * 9/5 + 32
        humidity = sensor.humidity
        print(f"Temp={temperature:0.1f}°F  Humidity={humidity:0.1f}%")
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(2.0)
    
