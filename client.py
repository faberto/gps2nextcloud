import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5010  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"[3G*7909378943*0009*LK,0,0,93]")
    print("Receiving...")
    data = s.recv(1024)
    print("Received", repr(data))
    s.sendall(b"[3G*7909378943*0002*LK]")
    print("Receiving...")
    data = s.recv(1024)
    print("Received", repr(data))
#    s.sendall(b"[SG*8800000015*008F*UD,220414,134652,A,22.571707,N,113.8613968,E,0.1,0.0,100,7,60,90,1000,50,0000,4,1,460,0,9360,4082,131,9360,4092,148,9360,4091,143,9360,4153,141]")
#    s.sendall(b"[SG*8800000015*0090*UD2,220414,134652,A,22.571707,N,113.8613968,E,0.1,0.0,100,7,60,90,1000,50,0000,4,1,460,0,9360,4082,131,9360,4092,148,9360,4091,143,9360,4153,141]")
    s.sendall(b"[3G*7909378943*00CA*UD,070619,234042,V,55.799770,N,37.9287083,E,0.00,0.0,0.0,0,100,92,0,0,00000010,7,255,250,2,9006,17108,144,9006,47361,149,9006,17102,137,9006,47366,137,9006,17103,136,9006,17107,132,9006,17163,126,0,28.7]")
    s.sendall(b"[3G*7909378943*00CA*UD,090619,232610,V,55.799485,N,37.9277517,E,0.00,0.0,0.0,0,100,32,0,0,00000010,7,255,250,2,9006,47361,147,9006,17102,136,9006,17103,129,9006,17108,128,9006,17163,126,9006,17107,122,9006,47366,119,0,23.8]")
#    s.sendall(b"[3G*7909378943*00C9*UD,110619,062651,A,55.799395,N,37.9284517,E,0.00,7.2,0.0,10,85,40,0,0,00000010,7,255,250,2,9006,17108,139,9006,47361,139,9006,17102,131,9006,47366,131,9006,17107,125,9006,17101,123,9006,47356,120,0,7.3]")
#    s.sendall(b"[3G*7909378943*00CD*UD,110619,062630,A,55.799328,N,37.9283800,E,0.00,220.2,0.0,10,100,41,0,0,00000010,7,255,250,2,9006,17108,145,9006,47361,142,9006,17107,133,9006,17102,133,9006,47366,130,9006,17101,125,9006,47356,124,0,13.0]")
