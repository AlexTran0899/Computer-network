import socket

def connect_to_server():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 1234))
    while True:
      data = s.recv(1024)
      if not data:
        break
      print(data.decode(), end='')
      guess = input()
      s.sendall(guess.encode())

if __name__ == "__main__":
  connect_to_server()
