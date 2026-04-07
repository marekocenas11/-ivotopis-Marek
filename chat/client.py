import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432


def receive_messages(client):
    """Přijímání zpráv ze serveru."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print('[Klient] Server se odpojil.')
                break
            if message == 'NICK':
                # Server žádá o přezdívku - zpracováno v main()
                continue
            print(message, end='')
        except Exception:
            print('[Klient] Ztraceno spojení se serverem.')
            break
    client.close()
    sys.exit(0)


def main():
    print('=' * 40)
    print('   Chatovací aplikace v Pythonu')
    print('   (Socket Programming)')
    print('=' * 40)
    print()

    nickname = input('Zadejte svou přezdívku: ').strip()
    if not nickname:
        nickname = 'Anonym'

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f'[Klient] Připojeno k serveru {HOST}:{PORT}')
        print('[Klient] Pro ukončení napište /quit')
        print('-' * 40)
    except ConnectionRefusedError:
        print('[Chyba] Nelze se připojit k serveru.')
        print('[Chyba] Ujistěte se, že server běží (python server.py)')
        sys.exit(1)

    # Počkat na požadavek přezdívky a odeslat ji
    try:
        msg = client.recv(1024).decode('utf-8')
        if msg == 'NICK':
            client.send(nickname.encode('utf-8'))
    except Exception:
        print('[Chyba] Chyba při odesílání přezdívky.')
        client.close()
        sys.exit(1)

    # Spustit vlákno pro přijímání zpráv
    receive_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    receive_thread.start()

    # Odesílání zpráv
    try:
        while True:
            message = input('')
            if message.strip().lower() == '/quit':
                print('[Klient] Odpojuji se...')
                client.close()
                break
            if message.strip():
                full_message = f'[{nickname}] {message}\n'
                client.send(full_message.encode('utf-8'))
    except (KeyboardInterrupt, EOFError):
        print('\n[Klient] Odpojuji se...')
        client.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
