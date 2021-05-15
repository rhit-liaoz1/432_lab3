# Get data from remote server, forward that data to a local client
import requests
import socket
import sys
import os
import _thread

url =""
addr =""

port = 6000

def getURL(url):
    try:
        req = requests.get(url = url)
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

    if len(sys.argv) < 1:
        print("Usage: Not enough arguments")
        sys.exit()
    else:
        port = int(sys.argv[1])

    host =''

    server_addr = (sys.argv[1], port)
    print("Escape character is '^]'.")
    message = input("->")



    # html = getURL(url)
    # create the socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind
        server_socket.bind((host, port))

        # listen
        server_socket.listen(10)

        print("Waiting for connections ...")
    except socket.error:
        print("error socket")
        if server_socket:
            server_socket.close()
        sys.exit(1)


    # accept
    while True:
        conn, address = server_socket.accept()

        _thread.start_new_thread(thread_helper,(conn, address))
        #might not neet close
        # server_socket.close()

        print("Connection from: " + str(address))
        message = input(" -> ")
        cmd = ""
        while str(cmd).strip() != '.':
            cmd = conn.recv(2048).decode()
            #cmd = str(message)
            if not cmd:
                break
            if len(str(cmd).split(" ")) != 3:
                conn.send("Invalid command format".encode())
                continue
            elif (cmd.startswith("GET")):
                url = cmd.split(" ")[1]
                addr = cmd.split(" ")[2]

                # conn.send("ready to transmit".encode())
                # response = conn.recv(2048).decode()
                # if (response == "ready"):
                #     fp = open(filename, 'r')
                #     data = fp.read(2048)
                #     conn.send(data.encode())
                #     fp.close()
            elif (cmd.startswith("exit") or cmd.startswith("^]")):
                print("see u!")
                break
            else:
                conn.send("Invalid command".encode())

        conn.close

def thread_helper(conn, address):

    rec = conn.recv(2024)

    # html = getURL(url)
    # url = rec.split('\n')[0].split(' ')[0]

    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((addr, port))
        soc.send(rec)
        data = socket.recv(2024).decode()
        fp = open("receive.txt", 'w')
        fp.write(data)
        fp.close()
        soc.close()
        conn.close()
    except socket.error:
        print("error socket")
        if soc:
            soc.close()
        sys.exit(1)




if __name__ == '__main__':
    main()