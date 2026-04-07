import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

clients = []
nicknames = []
lock = threading.Lock()


def broadcast(message, sender_client=None):
    """Odeslat zprávu všem klientům kromě odesílatele."""
    with lock:
        for client in clients:
            if client != sender_client:
                try:
                    client.send(message)
                except Exception:
                    remove_client(client)


def remove_client(client):
    """Odebrat klienta ze seznamu."""
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        broadcast(f'[Server] {nickname} opustil chat.\n'.encode('utf-8'))
        print(f'[Server] {nickname} se odpojil.')


def handle_client(client):
    """Zpracování zpráv od jednoho klienta."""
    while True:
        try:
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            decoded = message.decode('utf-8')
            print(decoded.strip())
            broadcast(message, client)
        except Exception:
            remove_client(client)
            break


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f'[Server] Chat server běží na {HOST}:{PORT}')
    print('[Server] Čekám na připojení klientů...')
    print('[Server] Pro ukončení stiskněte Ctrl+C')
    print('-' * 40)

    try:
        while True:
            client, address = server.accept()

            # Požádat klienta o přezdívku
            client.send('NICK'.encode('utf-8'))
            try:
                nickname = client.recv(1024).decode('utf-8').strip()
            except Exception:
                client.close()
                continue

            with lock:
                nicknames.append(nickname)
                clients.append(client)

            print(f'[Server] {nickname} se připojil z {address}')
            broadcast(f'[Server] {nickname} se připojil do chatu!\n'.encode('utf-8'))
            client.send('[Server] Vítejte v chatu! Napište zprávu a stiskněte Enter.\n'.encode('utf-8'))

            thread = threading.Thread(target=handle_client, args=(client,), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print('\n[Server] Ukončuji server...')
        with lock:
            for client in clients:
                client.close()
        server.close()
        sys.exit(0)


if __name__ == '__main__':
    main()
