import socket
import os

# configs:
FILES_DIR = "files"
DEFAULT_FILE = "index.html"
TIMEOUT = 1  
BUFFER_SIZE = 1024
def read_file(file_path):
    if file_path.endswith((".jpg", ".ico")):
        mode = "rb"  # read binary
    else:
        mode = "r"  # read text
    with open(file_path, mode) as f:
        return f.read()
def create_response(status, connection, content=None, location=None):
    headers = [
        f"HTTP/1.1 {status}",
        f"Connection: {connection}"
    ]
    if location:
        headers.append(f"Location: {location}")
    if content:
        headers.append(f"Content-Length: {len(content)}")
    headers.append("")  # empty line after the headers
    headers.append("")  # empty line before  the content
    response = "\r\n".join(headers).encode()
    if isinstance(content, bytes):
        response += content
    elif content:
        response += content.encode()
    return response
def run_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(5)


    while True:
        client_socket, client_address = server_socket.accept()
        client_socket.settimeout(TIMEOUT)
        handle_client(client_socket)
def handle_client(client_socket):
    try:
        while True:  
            request = b""
            while True:
                chunk = client_socket.recv(BUFFER_SIZE)
                if not chunk:  # empty request
                    client_socket.close()
                    return
                request += chunk
                if b"\r\n\r\n" in request:
                    break

            print(request.decode())  # print the request

            request_lines = request.decode().split("\r\n")
            first_line = request_lines[0]
            headers = {line.split(": ")[0]: line.split(": ")[1] for line in request_lines[1:] if ": " in line}
            connection = headers.get("Connection", "close")

			# procces of the request
            if first_line.startswith("GET"):
                path = first_line.split(" ")[1]
                if path == "/":
                    path = DEFAULT_FILE
                else:
                    path = path.lstrip("/")

                file_path = os.path.join(FILES_DIR, path)

                if os.path.exists(file_path):
                    content = read_file(file_path)
                    response = create_response("200 OK", connection, content)
                elif path == "redirect":
                    response = create_response("301 Moved Permanently", "close", location="/result.html")
                else:
                    response = create_response("404 Not Found", "close")
            else:
                response = create_response("400 Bad Request", "close")

			# send the request 
            client_socket.sendall(response)

            # close the socket if the connection is "close"
            if connection.lower() == "close":
                client_socket.close()
                return  # handle another client
            # if the connection is "keep-alive" we return in the loop for more iter
    #if we have timeout- close the socket
    except socket.timeout:
        print("Connection timed out.")
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    run_server(port)
