# דוגמה לקוד של הלקוח המתקבל פלט מהשרת ומדפיס אותו בפורמט הנכון
import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: client.py [serverIP] [serverPort]")
        return

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        domain = input("Enter domain: ")
        if domain == "exit":
            break
        sock.sendto(domain.encode(), (server_ip, server_port))
        response, _ = sock.recvfrom(1024)
        response = response.decode()
        if response.startswith("A,"):
            print(response.split(',')[1])  # רק ה-IP
        elif response.startswith("NS,"):
            print("Redirect to NS server at", response.split(',')[1])
        else:
            print(response)  # ידפיס 'non-existent domain' או תשובה אחרת

    sock.close()

if __name__ == "__main__":
    main()
