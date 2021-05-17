# Get data from remote server, forward that data to a local client
# import requests
import socket
import sys
import os
import threading
from urllib.parse import urlsplit

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

def parse_request(request):
    if request == '':
        return None, None
    split_request = request.split("\r\n")
    headers = {}
    for complete_header in split_request[1:]:
        if complete_header.strip() == "":
            continue
        header, value = complete_header.split(':', 1)
        headers[header] = value.strip()

    method, url, http_protocol = split_request[0].split(' ')
    return method, urlsplit(url), http_protocol, headers


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
        cmd = conn.recv(8192).decode()

        if not cmd:
            break

        method, url, http_ver, headers = parse_request(cmd)
        if method == 'GET':
            print(method, url, http_ver, headers)
            headers["Host"] = Host = url.netloc
            headers["Connection"] = "close"
            send_pa = f"{method} {url.path} {http_ver}\r\n"

            for header_key, header_value in headers.items():
                send_pa += f"{header_key}: {header_value}\r\n"
            send_pa += "\r\n"
            print(f"send_pa:\n{send_pa}")
            t = threading.Thread(target=_thread_helper, args=(conn, address, send_pa, Host))
            t.start()
        elif (cmd.startswith("exit") or cmd.startswith("^]")):
            print("see u!")
            conn.close()
            print("Closed connection from:", address)
            break
        else:
            conn.send("Invalid command".encode())
            conn.close()
            print("Closed connection from:", address)

    server_socket.close()

def _thread_helper(conn, address, se, Host):
    # print(conn)
    # rec = conn.recv(2024)
    # print(rec)
    # # html = getURL(url)
    # url = rec.split('\n')[0].split(' ')[1]
    # print("url:",url)
    # http  = url.find("://")
    # if (http==-1):
    #     temp = url
    # else:
    #     temp = url[(http+3):]
    # pp = temp.find(":")
    # # find web server
    # webserver_pos = temp.find("/")
    # if webserver_pos == -1:
    #     webserver_pos = len(temp)
    # webserver = ""
    # port = -1
    # if (pp == -1 or webserver_pos < pp):
    #     port = 4000
    #     webserver = temp[:webserver_pos]
    # else:
    #     port = int((temp[(pp + 1):])[:webserver_pos - pp - 1])
    #     webserver = temp[:pp]
    print("host:", Host)
    # connect to webserver
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("error socket: webserver")
        if server_socket:
            server_socket.close()
        sys.exit(1)
        
    websiteIP = socket.gethostbyname(Host)
    try:
        # bind
        server_socket.connect((websiteIP, 80))
    except socket.error:
        print("error connection: webserver")
        if server_socket:
            server_socket.close()
        sys.exit(1)

        # forward message to website
    try:
        server_socket.send(se.encode())
    except socket.error:
        print("error send: webserver")
        if server_socket:
            server_socket.close()
        sys.exit(1)
        
    print("Sent data to website")
    
    try:
        # receive data from website
        data = server_socket.recv(8192)
        print("Receive data from website",data)
        # send data from web server to client
        conn.send(data)
        conn.close()
        print("Closed connection from:", address)
    except socket.error:
        print("error socket")
        if server_socket:
            server_socket.close()
        sys.exit(1)
    

    
    

#    while True:
#        try:
#            # receive data from website
#            data = server_socket.recv(2024).decode()
#            print("Receive data from website",data)
#			# send data from web server to client
#            conn.send(data.encode())
#        except socket.error:
#            print("error socket")
#            if server_socket:
#                server_socket.close()
#            sys.exit(1)
    




if __name__ == '__main__':
    main()

