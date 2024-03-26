import socket
import threading

SECRET_WORD = 'arkansas'
MAX_INCORRECT_GUESSES = 7
word_progress = ['_' for _ in SECRET_WORD]

def hangman_game(connection, addr, attempts):
  while attempts < MAX_INCORRECT_GUESSES and '_' in word_progress:
    msg = f"Word: {' '.join(word_progress)}\nGuess a letter: "
    connection.sendall(msg.encode())
    guess = connection.recv(1024).decode().strip().lower()

    if len(guess) != 1 or not guess.isalpha():
      connection.sendall("Please guess a single letter.\n".encode())
      continue

    if guess in SECRET_WORD:
      for index, letter in enumerate(SECRET_WORD):
        if letter == guess:
          word_progress[index] = guess
    else:
      attempts += 1
      connection.sendall(f"Incorrect. {MAX_INCORRECT_GUESSES - attempts} guesses remaining.\n".encode())

    if '_' not in word_progress:
      connection.sendall(f"Congratulations! You guessed the word: {''.join(word_progress)}\n".encode())
      break

  if attempts >= MAX_INCORRECT_GUESSES:
    connection.sendall(f"Sorry, you've been hung. The word was: {SECRET_WORD}\n".encode())

def client_thread(conn, addr,attempts):
  print(f"Connected by {addr}")
  hangman_game(conn, addr, attempts)

def start_server():
  attempts = 0
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 1234))
    s.listen()
    while True:
      conn, addr = s.accept()
      thread = threading.Thread(target=client_thread, args=(conn, addr,attempts))
      thread.start()

if __name__ == "__main__":
  start_server()
