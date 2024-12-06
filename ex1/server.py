import socket
import sys

def load_zone(filename):
    # map for domains and records-
    zone = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(',')
                domain = parts[0]
                # take the ip and the type(A or NS)
                record = {'address': parts[1], 'type': parts[2]}
                zone[domain] = record
    return zone

def find_record(zone, domain):
    # if the domain is in the zone file, return the addres.
    if domain in zone:
        return zone[domain]
    # if this domain isnt in the zone file, check if the NS is "substring" of the domain 
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
    zone = load_zone(zonefile)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    
    
    try:
        while True:
            # get the domain from the resolver:
            data, addr = sock.recvfrom(512)  
            domain = data.decode().strip()
            
            record = find_record(zone, domain)
            if record:
                response = f"{record['type']},{record['address']},{domain}"
            else:
                response = "non-existent domain"
            
            sock.sendto(response.encode(), addr)
    except KeyboardInterrupt:
        print("")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
