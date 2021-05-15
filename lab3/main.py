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
    host = socket.gethostname()
    print("Host name: " + str(host))

    if len(sys.argv) != 3:
        print("Usage: python client.py <server_IP> <server_port>")
        sys.exit()

    port = int(sys.argv[2])

    server_addr = (sys.argv[1], port)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(server_addr)

    message = input("->")

    while message.strip() != ".":
        cmd = str(message)
        if cmd.startswith("exit"):
            print("see u!")
            break
        url = cmd.split(" ")[1]


        # Check for if a file exists
        # if cmd.startswith("utake"):
        #     if not os.path.exists(fileName):
        #         print(fileName + " doesn't exist")
        #         message = input(" -> ")
        #         continue

        client_socket.send(cmd.encode())
        response = client_socket.recv(1024).decode()
        getURL(url);

        if response == "ready to transmit":
            client_socket.send("ready".encode())

        elif response == "ready to receive":
            client_socket.send("")


        else:
            print(response)

        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    main()