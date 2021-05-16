import socket
import sys
import os


port = 6000


def client():
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
        if (cmd.startswith("GET")):
            if len(str(cmd).split(" ")) != 3:
                print("Invalid command format")
                break
            else:
                url = cmd.split(" ")[1]
                addr = cmd.split(" ")[2]


        client_socket.send(cmd.encode())
        response = client_socket.recv(2024).decode()

        # if response == "ready to transmit":
        dir = "received_files/" + "rec.txt"
        # client_socket.send("ready".encode())
        fp = open(dir, 'w')
        data = client_socket.recv(2048).decode()
        fp.write(data)
        fp.close()
        # else:
        print(response)

        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    client()
