from socket import * # Import socket library, does not need to iterate socket. ~~
from time import time # Import time library to track timestamps, does not need to iterate time. ~~
import random

def heartbeat_udpserver():
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('localhost', 44518))
    server_socket.settimeout(50) # Set a timeout for recvfrom to prevent infinite blocking
    print("UDP Heartbeat Server is running...")

    last_heartbeat_map = {}  # Dictionary to store the last heartbeat time for each client. 
    seq_tracker_map = {} # Dictionary to track sequence numbers for each client (for packet loss calculation). 
    client_heartbeat_timeout = 2 # Time (in seconds) after which a client is considered disconnected. 

    while True:
        try:
            data, address = server_socket.recvfrom(1024)
            message = data.decode()
            current_time = time()

            client_seq, sent_time = map(float, message.split()[1:]) # Extract the sequence number and the time the message was sent
            latency = current_time - sent_time
            
            # Random packet loss simulation (30% loss probability)
            if random.random() < 0.3:
                print(f"Simulated packet loss for {address} | Seq: {int(client_seq)}")
                continue

            # Update the last heartbeat time for the client
            last_heartbeat_map[address] = current_time #address -> key, current_time -> value / add or update dictionary

            # Initialize the sequence tracker for new clients
            if address not in seq_tracker_map:
                seq_tracker_map[address] = [] #list for value of dictionary
            seq_tracker_map[address].append(int(client_seq)) # add current client's sequence number to list of address

            print(f"Heartbeat received from {address} | Seq: {int(client_seq)} | Latency: {latency:.4f} seconds")

            ack_msg = f"ACK {int(client_seq)} {latency:.4f}"
            server_socket.sendto(ack_msg.encode(), address)
            
            
            # Check for disconnected clients
            for client, last_time in list(last_heartbeat_map.items()): 
                if current_time - last_time > client_heartbeat_timeout:
                    print(f"Client {client} has disconnected. Calculating packet loss...")

                    if client in seq_tracker_map:
                        seq_list = seq_tracker_map[client]
                        if seq_list:
                            # Calculate packet loss
                            total_packets = max(seq_list) - min(seq_list) + 1
                            lost_packets = total_packets - len(seq_list)
                            print(f"Client {client} Packet Loss: {lost_packets}/{total_packets} ({(lost_packets/total_packets)*100:.2f}%)")
                        del seq_tracker_map[client] # Remove the client's sequence data after processing
                    del last_heartbeat_map[client]  # Remove the client's last Heartbeat data to clean up inactive clients
        
        except KeyboardInterrupt: # enter Ctrl C to stop the program
            print("Shutting down server.")
            break # Exit the loop on a keyboard interrupt (Ctrl+C)

    
    server_socket.close()
    print("Socket closed.")

if __name__ == "__main__":
    heartbeat_udpserver()

