import socket
import struct

def send_msg(sock: socket.socket, data: bytes) -> None:
    header = struct.pack(">H", 3)
    type = struct.pack(">H", 1)
    length = struct.pack(">H", 4)
    sock.sendall(header + type + length + data)

def recv_msg(sock: socket.socket) -> bytes:
    raw_header = _recvn(sock, 3)
    msg_len = struct.unpack(">I", raw_header)[0]
    raw_type = _recvn(sock, 1)
    msg_len = struct.unpack(">I", raw_type)[0]
    raw_length = _recvn(sock, 4)
    msg_len = struct.unpack(">I", raw_length)[0]

    return _recvn(sock, msg_len) + f"{str(raw_header)}, {str(raw_type)}, {str(raw_length)}"


def _recvn(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before message was complete")
        buf.extend(chunk)
    return bytes(buf)