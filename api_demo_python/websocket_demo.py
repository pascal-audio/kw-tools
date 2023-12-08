# Requires Websockets
# to install: pip install websockets

from websockets.sync.client import connect

TARGET = '192.168.64.100'

def get_all():
    with connect(f"ws://{TARGET}/ws") as websocket:
        cmd = "GET *"
        websocket.send(cmd)

        reply = websocket.recv(timeout=0.5)
        print(reply)
        
        websocket.close_socket()

def subscribe_all():
    with connect(f"ws://{TARGET}/ws") as websocket:
        cmd = "SUBSCRIBE *"
        websocket.send(cmd)

        for i in range(5):
            reply = websocket.recv(timeout=0.5)
            print(reply)
        
        websocket.close_socket()

get_all()
subscribe_all()