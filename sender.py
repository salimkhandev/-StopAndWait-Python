import socket
import time
import random

# Create UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_ip = "127.0.0.1"
receiver_port = 12345
sender_socket.settimeout(3)  # Timeout for retransmission (3 sec)

seq_num = 0  # Sequence number (0 or 1)

while True:
    message = f"{seq_num}::Hello"
    print(f"📤 Sending: {message}")

    sender_socket.sendto(message.encode(), (receiver_ip, receiver_port))

    try:
        ack, _ = sender_socket.recvfrom(1024)
        ack_num = int(ack.decode().split("::")[1])

        if ack_num == seq_num:  # Correct ACK received
            print(f"✅ ACK {ack_num} received, moving to next packet.")
            seq_num = 1 - seq_num  # Toggle sequence number
        else:
            print(f"⚠️ Incorrect ACK {ack_num}, retransmitting...")

    except socket.timeout:
        print(f"⏳ Timeout! No ACK received, retransmitting {message}...")

    time.sleep(1)  # Simulate delay before sending next packet
