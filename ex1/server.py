import socket
import sys

def load_zone_file(filename):
    zone = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # כדי להתעלם משורות ריקות
                domain, address, record_type = line.strip().split(',')
                zone[domain] = (address, record_type)
    return zone

def main():
    if len(sys.argv) != 3:
        print("Usage: server.py [PORT] [ZONEFILE]")
        return
    
    port = int(sys.argv[1])
    zonefile = sys.argv[2]
    zone = load_zone_file(zonefile)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    
    print(f"DNS server is up and listening on port {port}")
    
    try:
        while True:
            data, addr = sock.recvfrom(512)  # 512 bytes buffer size
            domain = data.decode().strip()
            if domain in zone:
                address, record_type = zone[domain]
                response = f"{record_type},{address},{domain}"
            else:
                response = "non-existent domain"
            
            sock.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        print("Shutting down server")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
