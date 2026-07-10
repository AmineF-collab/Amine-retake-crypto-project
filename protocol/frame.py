import socket
import struct

def send_msg(sock: socket.socket, data: bytes) -> None:
    header = b"SFX"
    type = struct.pack(">B", 1)
    length = struct.pack(">I", 4)
    sock.sendall(header + type + length + data)

def recv_msg(sock: socket.socket) -> bytes:
    raw_header = _recvn(sock, 3)
    if raw_header != b"SFX":
        raise ValueError("Mauvais header de frame")
    msg_len = struct.unpack(">I", raw_header)[0]
    raw_type = _recvn(sock, 1)
    msg_len = struct.unpack(">B", raw_type)[0]
    raw_length = _recvn(sock, 4)
    msg_len = struct.unpack(">I", raw_length)[0]
    payload = _recvn(sock, msg_len)
    return msg_len, payload


def _recvn(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before message was complete")
        buf.extend(chunk)
    return bytes(buf)