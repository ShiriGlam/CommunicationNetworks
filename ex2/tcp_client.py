import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.229.132', 12345))
s.send(b'Shiri Glam')
data = s.recv(100)
print("Server sent: ", data)
id_number = '213074628'
s.send(id_number.encode())
data_id = s.recv(100)
print("Server sent: ", data_id)
s.close()