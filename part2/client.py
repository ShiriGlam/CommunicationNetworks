import socket
import sys
import os

def save_resource(file_path, content):
    # חילוץ שם הקובץ בלבד
    file_name = os.path.basename(file_path)
    counter = 1
    base_name, ext = os.path.splitext(file_name)
    while os.path.exists(file_name):
        file_name = f"{base_name}_{counter}{ext}"
        counter += 1
    # שמירת תוכן הקובץ
    with open(file_name, "wb") as f:
        f.write(content)


def extract_content(response):
    # פיצול ה-response לשני חלקים: headers ותוכן
    headers, _, body = response.partition(b"\r\n\r\n")
    return headers.decode(), body

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

        # יצירת חיבור לשרת
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((server_ip, server_port))

            # שליחת בקשת GET לשרת
            request = f"GET {file_path} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: close\r\n\r\n"
            client_socket.sendall(request.encode())

            # קבלת התשובה מהשרת
            response = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                response += chunk

            # חילוץ headers והתוכן
            headers, content = extract_content(response)

            # הדפסת השורה הראשונה של ה-response
            first_line = headers.split("\r\n")[0]
            print(first_line)

            # שמירת תוכן הקובץ
            if first_line.startswith("HTTP/1.1 200 OK"):
                save_resource(file_path, content)
            else:
                print(f"Error: {first_line}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
