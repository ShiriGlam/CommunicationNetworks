import socket
import sys
import time

def main():
    if len(sys.argv) != 5:
        print("Usage: resolver.py [myPort] [parentIP] [parentPort] [cacheTime]")
        return

    my_port = int(sys.argv[1])
    parent_ip = sys.argv[2]
    parent_port = int(sys.argv[3])
    cache_time = int(sys.argv[4])

    cache = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', my_port))

    print(f"Resolver server is up and listening on port {my_port}")
    
    try:
        while True:
            data, addr = sock.recvfrom(512)
            domain = data.decode().strip()
            if domain in cache and (time.time() - cache[domain][1]) < cache_time:
                response = cache[domain][0]
            else:
                parent_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                parent_sock.sendto(domain.encode(), (parent_ip, parent_port))
                response, parent_addr = parent_sock.recvfrom(512)
                cache[domain] = (response.decode(), time.time())
                parent_sock.close()
            
            sock.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        print("Shutting down resolver")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
