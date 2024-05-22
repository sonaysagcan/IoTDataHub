import random
import time
import json
import socket
from config import TCP_SERVER_PORT, TCP_SERVER_HOST

"""
    Iot cihazının Tcp sunucumuza mesaj gönderme işlemini simule eder.
"""
def run():

    count = 0
    while count < 10000:

        message ={
          "device_uid": random.randint(0, 999999),
          "lat": random.uniform(-90, 90),
          "long": random.uniform(-180, 180),
          "time": time.time()
        }
        json_message = json.dumps(message) + '\n'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
            count+= 1
            print(f'{count}')

            s.sendall(json_message.encode())
            time.sleep(0.01)

if __name__ == "__main__":
    run()

