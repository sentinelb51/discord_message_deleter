# Stub out audioop for Python 3.13 (no voice support)
from py313_monkeypatch import monkeypatch
monkeypatch()

import sys
from discord.errors import LoginFailure
from client import Client

def main():
    client: Client = Client(
        sync_presence=False,
        assume_unsync_clock=False,
        chunk_guilds_at_startup=False,
    )

    try:
        token = input("Enter token: ")
        if not token:
            print("No token provided; exiting.")
            sys.exit(1)
        client.run(token)
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(1)
    except LoginFailure:
        print("[!] Login failed; invalid token provided.")
        sys.exit(1)

if __name__ == "__main__":
    main()
