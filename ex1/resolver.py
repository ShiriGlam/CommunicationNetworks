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

    try:
        while True:
            data, addr = sock.recvfrom(512)
            domain = data.decode().strip()
            print(f"Received domain request: {domain} from {addr}")

            response = resolve_domain(domain, parent_ip, parent_port, cache, cache_time)
            sock.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        print("Shutting down resolver")
    finally:
        sock.close()

def resolve_domain(domain, parent_ip, parent_port, cache, cache_time):
    if domain in cache and (time.time() - cache[domain][1]) < cache_time:
        return cache[domain][0]
    else:
        response, new_ip, new_port = recursive_query(domain, parent_ip, parent_port)
        cache[domain] = (response, time.time())
        return response

def recursive_query(domain, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(domain.encode(), (ip, port))
    response, _ = sock.recvfrom(512)
    response = response.decode()

    # If an NS record is found, recursively query the indicated server
    if "NS" in response:
        ns_info = response.split(',')[1]
        ns_ip, ns_port = ns_info.split(':')
        print(f"Received ns port: {ns_port} and ns_ip: {ns_ip}")
        return recursive_query(domain, ns_ip, int(ns_port))
    
    sock.close()
    return response, ip, port

if __name__ == "__main__":
    main()

