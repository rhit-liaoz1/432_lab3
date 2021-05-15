# Get data from remote sercver
import requests
import socket
import sys
import os

url =""
addr =""

def getURL(url):
    h = {}
    try:
        req = requests.get(url = url, headers =h)
        if req.status_code == 200:
            print('Success.')
            html = req.text
            return html
        else:
            exit('Can not get the website.')
    except ConnectionError:
         exit('ConnectionError.')


def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_IP> <server_port>")
        sys.exit()

    port = int(sys.argv[2])

    server_addr = (sys.argv[1], port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_addr)

    message = input(" -> ")

    while message.strip() != ".":
        cmd = str(message)
        if cmd.startswith("exit"):
            print("see u!")
            break
        fileName = cmd.split(" ")[1]


        # Check for if a file exists
        if cmd.startswith("utake"):
            if not os.path.exists(fileName):
                print(fileName + " doesn't exist")
                message = input(" -> ")
                continue

        client_socket.send(cmd.encode())
        response = client_socket.recv(1024).decode()

        if response == "ready to transmit":
            dir = input(""" Enter your save directory:
                            -> """)
            if (dir == ""):
                dir = "received_files/" + fileName
            client_socket.send("ready".encode())
            fp = open(dir, 'w')
            data = client_socket.recv(2048).decode()
            fp.write(data)
            fp.close()
        elif response == "ready to receive":
            fp = open(fileName)
            data = fp.read(2024)
            client_socket.send(data.encode())
            fp.close()

        else:
            print(response)

        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    main()