import socket
import time
import random

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(("127.0.0.1", 12345))

expected_seq_num = 0  # Sequence number to expect

while True:
    data, sender_addr = receiver_socket.recvfrom(1024)
    received_msg = data.decode()
    seq_num = int(received_msg.split("::")[0])  # Extract sequence number

    if random.random() < 0.3:  # Simulate 30% packet loss
        print(f"❌ Packet {seq_num} lost, ignoring...")
        continue

    if seq_num == expected_seq_num:  # Correct sequence received
        print(f"📩 Received: {received_msg}")

        time.sleep(random.uniform(0.5, 2))  # Simulate delayed ACK
        ack_msg = f"ACK::{seq_num}"
        receiver_socket.sendto(ack_msg.encode(), sender_addr)
        print(f"✅ Sent: {ack_msg}")

        expected_seq_num = 1 - expected_seq_num  # Toggle expected sequence number
    else:
        print(f"⚠️ Duplicate or out-of-order packet {seq_num}, resending last ACK...")
        ack_msg = f"ACK::{1 - expected_seq_num}"  # Send last valid ACK
        receiver_socket.sendto(ack_msg.encode(), sender_addr)
