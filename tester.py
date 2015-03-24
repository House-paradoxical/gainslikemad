from clientpy2 import *
from tick_info import *
import socket
import sys
import re

HOST, PORT = "codebb.cloudapp.net", 17429
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
run(sock,"MY_SECURITIES")
run(sock,"MY_CASH")
