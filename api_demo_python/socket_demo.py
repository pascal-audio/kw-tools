import socket

TARGET = '192.168.64.100'
PORT = 7621

def get_all():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TARGET, PORT))
        
        cmd = "GET *\n"
        s.sendall(cmd.encode())

        while True:
            reply = s.recv(64*1024)

            if reply:
                reply = reply.decode()
                print(reply)

            if not reply or f'*{cmd}' in reply:
                break

        
def subscribe_all():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TARGET, PORT))
        
        cmd = "SUBSCRIBE *\n"
        s.sendall(cmd.encode())

        for i in range(5):
            reply = s.recv(64*1024)

            if reply:
                reply = reply.decode()
                print(reply)


get_all()
subscribe_all()