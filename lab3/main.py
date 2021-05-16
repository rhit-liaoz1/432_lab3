# Get data from remote server, forward that data to a local client
# import requests
import socket
import sys
import os
import _thread

Host =""
get =""

port = 6000

# def getURL(url):
#     try:
#         req = requests.get(url = url)
#         if req.status_code == 200:
#             print('Success.')
#             html = req.text
#             return html
#         else:
#             exit('Can not get the website.')
#     except ConnectionError:
#          exit('ConnectionError.')

def main():
    host = socket.gethostname()
    print("Host name: " + str(host))

    if len(sys.argv) < 2:
        print("Usage: Not enough arguments")
        sys.exit()
    else:
        port = int(sys.argv[1])

    host =''

    server_addr = (sys.argv[1], port)
    print("Escape character is '^]'.")

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

        #start a new thread by calling thread_helper function
        #might not neet close
        print("Connection from: " + str(address))
        # server_socket.close()
        cmd = ""
        while str(cmd).strip() != '.':
            cmd = conn.recv(2048).decode()
            print(cmd)
            if not cmd:
                break
            if len(str(cmd).split(" ")) != 3:
                conn.send("Invalid command format".encode())
                continue
            if (cmd.startswith("GET")):
                if len(str(cmd).split(" ")) != 3:
                    conn.send("Invalid command format".encode())
                    continue
                else:
                    Host = cmd.split(" ")[1]
                    # cmd.split(" ")[2]
                    get = "/ HTTP/1.0"
                    send_pa = Host + "\n" + get + "\n" + "Connection: close"
                    _thread.start_new_thread(thread_helper, (conn, address, send_pa))
            elif (cmd.startswith("exit") or cmd.startswith("^]")):
                print("see u!")
                break
            else:
                conn.send("Invalid command".encode())

        server_socket.close()

def thread_helper(conn, address, se):
    # print(conn)
    rec = conn.recv(2024)
    print(rec)
    # # html = getURL(url)
    url = rec.split('\n')[0].split(' ')[1]
    print("url:",url)
    http  = url.find("://")
    if (http==-1):
        temp = url
    else:
        temp = url[(http+3):]
    pp = temp.find(":")
    # find web server
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)
    webserver = ""
    port = -1
    if (pp == -1 or webserver_pos < pp):
        port = 4000
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(pp + 1):])[:webserver_pos - pp - 1])
        webserver = temp[:pp]

    # connect to webserver
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind
        server_socket.connect((webserver, port))

        # listen
        server_socket.send(se)

        while True:
            try:
                # send data from web server to client
                data = socket.server_socket(2024).decode()
                conn.send(data)
            except socket.error:
                print("error socket")
                if server_socket:
                    server_socket.close()
                sys.exit(1)
    except socket.error:
        print("error socket")
        if server_socket:
            server_socket.close()
        sys.exit(1)




if __name__ == '__main__':
    main()