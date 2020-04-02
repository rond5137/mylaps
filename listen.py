import socket

sock = socket.socket()
sock.bind(('', 3097))
sock.listen(1)
conn, addr = sock.accept()

while True:
    try:
        data = conn.recv(2048)
        if not data:
            print('NO DATA')
            break
        else:
            print(data)
            d = data.decode('utf8')
            # n = d.replace(r'\r\n', '')[len(d)-4:]
            parse = d.split('@')
            # print(parse)
            n = parse[-2]
            print(f'{n=}')
            conn.send(f'RondServer@AckPassing@{n}@$'.encode())
        if b'@Pong@' in data:
            conn.send(b'RondServer@AckPong@Version2.1@$')
        # conn.send(data.upper())
        # conn.send(b'hello')
        # conn.send(b'RondServer@GetInfo@office@$')
    except KeyboardInterrupt:
        i = input('input:')
        if i:
            conn.send(i.encode())
        else:
            break
conn.close()
