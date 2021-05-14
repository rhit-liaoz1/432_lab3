import socket
import sys
import os

port = 4000
def server():
    # get the hostname
    host = socket.gethostname()
    print("Host name: " + str(host))

    # host = 'localhost'
    if(len(sys.argv) != 2):
        print("Usage: python server.py <port_number>")
        sys.exit()
    elif (len(sys.argv) == 1):
        port = 4000
    else:
        port = int(sys.argv[1])

    # create the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #bind
    server_socket.bind((host, port))

    #listen
    server_socket.listen(5)

    print("Wating for connections ...")
    # accept
    while True:
        conn, address = server_socket.accept()

        print("Connection from: " + str(address))

        cmd = ""
        while str(cmd).strip() != '.':
            cmd = conn.recv(2048).decode()
            if not cmd:
                break
            if len(str(cmd).split(" ")) != 2:
                conn.send("Invalid command format".encode())
                continue
            filename = cmd.split(" ")[1]
            if(cmd.startswith("iwant")):
                if(not os.path.exists(filename)):
                    conn.send("Requested file not found.".encode())
                    continue

                conn.send("ready to transmit".encode())
                response = conn.recv(2048).decode()
                if(response == "ready"):
                    fp = open(filename, 'r')
                    data = fp.read(2048)
                    conn.send(data.encode())
                    fp.close()
            elif(cmd.startswith("utake")):
                if(os.path.exists("received_files/"+filename)):
                    conn.send("file already existed".encode())
                    continue
                conn.send("ready to receive".encode())
                fp = open("received_files/"+filename,'w')
                data = conn.recv(2048).decode()
                fp.write(data)
                fp.close()
            else:
                conn.send("Invalid command".encode())



        conn.close


if __name__ == '__main__':
    server()
