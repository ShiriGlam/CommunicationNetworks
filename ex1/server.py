import socket
import sys

def load_zone_file(filename):
    zone = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(',')
                domain = parts[0]
                record = {'address': parts[1], 'type': parts[2]}
                zone[domain] = record
    return zone

def find_record(zone, domain):
    if domain in zone:
        return zone[domain]
    else:
        for d, rec in zone.items():
            if rec['type'] == 'NS' and domain.endswith(d):
                return rec
    return None

def main():
    if len(sys.argv) != 3:
        print("Usage: server.py [PORT] [ZONEFILE]")
        return
    
    port = int(sys.argv[1])
    zonefile = sys.argv[2]
    zone = load_zone_file(zonefile)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    
    print(f"DNS server listening on port {port}")
    
    try:
        while True:
            data, addr = sock.recvfrom(512)  
            domain = data.decode().strip()
            print(f"Received query for domain: {domain} from {addr}")
            
            record = find_record(zone, domain)
            if record:
                response = f"{record['type']},{record['address']},{domain}"
            else:
                response = "non-existent domain"
            
            print(f"Sending response: {response}")
            sock.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        print("Shutting down server")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
