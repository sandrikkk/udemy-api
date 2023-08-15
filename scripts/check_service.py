# check_service.py

import argparse
import socket
import time

# Check if port is open, avoid docker-compose race condition

parser = argparse.ArgumentParser(
    description="Check if port is open, avoid docker-compose race condition"
)
parser.add_argument("--service-name", required=True)
parser.add_argument("--ip", required=True)
parser.add_argument("--port", required=True)

args = parser.parse_args()

# Get arguments
SERVICE_NAME = str(args.service_name)
PORT = int(args.port)
IP = str(args.ip)

# Infinite loop
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((IP, PORT))
    if result == 0:
        print(
            "Port is open! Bye! Service:{} Ip:{} Port:{}".format(SERVICE_NAME, IP, PORT)
        )
        break
    else:
        print(
            "Port is not open! I'll check it soon! Service:{} Ip:{}"
            "Port:{}".format(SERVICE_NAME, IP, PORT)
        )
        time.sleep(5)
