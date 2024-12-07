import socket
import time
# יצירת חיבור
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.229.132', 12345))
name = "Shiri Glam\n"
s.send(name.encode())
# קבלת תגובה רצופה לשתי ההודעות
response1 = s.recv(512)# שליחת הודעה שנייה עם תו מפריד בסוף
id_number = "213074628\n"
s.send(id_number.encode())

response2 = s.recv(512)

time.sleep(2)
# הדפסת תגובות נפרדות
print("Server response for name: ", response1)
print("Server response for ID number: ", response2)

# סגירת חיבור
s.close()
