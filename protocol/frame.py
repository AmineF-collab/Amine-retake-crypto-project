import socket
import struct
max_payload=1_048_576
def send_msg(sock: socket.socket,message_type:int, data: bytes) -> None:
    header = b"SFX"
    type = struct.pack(">B", message_type)
    length = struct.pack(">I", len(data))
    sock.sendall(header + type + length + data)

def recv_msg(sock: socket.socket) -> bytes:
    raw_header = _recvn(sock, 3)
    if raw_header != b"SFX":
        raise ValueError("Bad header of frame")
    raw_type = _recvn(sock, 1)
    msg_type = struct.unpack(">B", raw_type)[0]
    raw_length = _recvn(sock, 4)
    msg_len = struct.unpack(">I", raw_length)[0]
    if msg_len > max_payload:
        raise ValueError("Payload too large")
    payload = _recvn(sock, msg_len)
    return msg_type, payload


def _recvn(sock: socket.socket, n: int) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before message was complete")
        buf.extend(chunk)
    return bytes(buf)