from typing import Optional

server_dir: Optional[str] = None


def set_server_dir(_dir: str):
    global server_dir
    server_dir = _dir
