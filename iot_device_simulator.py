import random
import time
import json
import socket
from config import TCP_SERVER_PORT, TCP_SERVER_HOST, log

"""
    Iot cihazının Tcp sunucumuza mesaj gönderme işlemini simule eder.
"""
def run():

    while True:
        count = 0
        while count < 1000:
            message ={
              "device_uid": random.randint(0, 999999),
              "lat": random.uniform(-90, 90),
              "long": random.uniform(-180, 180),
              "created_at": time.time()
            }
            json_message = json.dumps(message) + '\n'
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))
                    count+= 1
                    log.info(f'iot_device_simulator send:{message}')

                    s.sendall(json_message.encode())
                    time.sleep(0.01)
            except ConnectionRefusedError:
                log.error("Connection refused by the server.")
                break
            except TimeoutError:
                log.error("Connection timed out.")
                break
            except socket.error as e:
                log.error(f"Socket error: {str(e)}")
                break
            except Exception as e:
                log.error(f"An unexpected error occurred: {str(e)}")
                break

        time.sleep(5)

if __name__ == "__main__":
    run()

