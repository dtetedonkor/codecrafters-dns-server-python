import socket
import struct


def main():
    # DNS header fields
    ID = 1234

    QR = 1
    OPCODE = 0
    AA = 0
    TC = 0
    RD = 0
    RA = 0
    Z = 0
    RCODE = 0

    QDCOUNT = 0
    ANCOUNT = 0
    NSCOUNT = 0
    ARCOUNT = 0

    # Combine the individual flag fields into one 16-bit value
    flags = (
        (QR << 15)
        | (OPCODE << 11)
        | (AA << 10)
        | (TC << 9)
        | (RD << 8)
        | (RA << 7)
        | (Z << 4)
        | RCODE
    )

    # Six 16-bit unsigned integers, big-endian
    packer = struct.Struct(">HHHHHH")

    packed_data = packer.pack(
        ID,
        flags,
        QDCOUNT,
        ANCOUNT,
        NSCOUNT,
        ARCOUNT
    )

    # Create UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Listen on port 2053
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            # Receive DNS query
            buf, source = udp_socket.recvfrom(512)

            # Send our DNS response
            udp_socket.sendto(packed_data, source)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()