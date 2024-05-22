import os
from dotenv import load_dotenv
import logging as log

log.getLogger().setLevel(log.INFO)
log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
TCP_SERVER_PORT = int(os.getenv("TCP_SERVER_PORT"))
TCP_SERVER_HOST = os.getenv("TCP_SERVER_HOST")
LOCATION_Q = os.getenv("LOCATION_Q")