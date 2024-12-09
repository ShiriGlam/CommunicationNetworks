import socket
import sys
import os
def save_resource(file_path, content):
    if file_path == "/" :
        file_name = "index.html"
    else:
        # חילוץ שם הקובץ בלבד
        file_name = os.path.basename(file_path)
    # שמירת תוכן הקובץ
    with open(file_name, "wb") as f:
        f.write(content)


def extract_content(response):
    # פיצול ה-response לשני חלקים: headers ותוכן
    headers, _, body = response.partition(b"\r\n\r\n")
    return headers.decode(), body


def send_request(server_ip, server_port, file_path):
    """שולח בקשה לשרת ומחזיר את התגובה"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        # שליחת בקשת GET לשרת
        request = f"GET {file_path} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: Keep-Alive\r\n\r\n"
        client_socket.sendall(request.encode())

        # קבלת התשובה מהשרת
        response = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            response += chunk
        return response
    finally:
        client_socket.close()


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    while True:
        # קלט נתיב מהמשתמש
        file_path = input("Enter the file path to request (or 'exit' to quit): ").strip()
        if file_path.lower() == "exit":
            break

        try:
            # שליחת בקשה וקבלת תגובה
            response = send_request(server_ip, server_port, file_path)

            # חילוץ headers והתוכן
            headers, content = extract_content(response)

            # הדפסת השורה הראשונה של ה-response
            first_line = headers.split("\r\n")[0]
            print(first_line)

            # טיפול בתגובת 301 Moved Permanently
            if first_line.startswith("HTTP/1.1 301"):
                location = None
                for line in headers.split("\r\n"):
                    if line.startswith("Location:"):
                        location = line.split(":", 1)[1].strip()
                        break
                if location:
                    # שליחת בקשה חדשה לכתובת ההפניה
                    response = send_request(server_ip, server_port, location)
                    headers, content = extract_content(response)
                    first_line = headers.split("\r\n")[0]
                    print(first_line)
                    if first_line.startswith("HTTP/1.1 200 OK"):
                        save_resource(location, content)
                continue  # המשך לבקשה הבאה

            # שמירת תוכן הקובץ במקרה של 200 OK
            if first_line.startswith("HTTP/1.1 200 OK"):
                save_resource(file_path, content)
            else:
                print(f"Error: {first_line}")

        except Exception as e:
            print(f"Error: {e}")



if __name__ == "__main__":
    main()
