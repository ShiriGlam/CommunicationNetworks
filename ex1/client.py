import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: client.py [serverIP] [serverPort]")
        return

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            domain = input("Enter domain: ")
            sock.sendto(domain.encode(), (server_ip, server_port))
            response, server = sock.recvfrom(512)
            print(response.decode())
    except KeyboardInterrupt:
        print("Client shutting down")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
