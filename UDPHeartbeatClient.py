from socket import *
from time import time, sleep
import random # I should put random. before using random module.

def heartbeat_udpclient():
    server_address = ("localhost", 44518) 
    client_socket = socket(AF_INET, SOCK_DGRAM) 

    seq_number = 1 
    rtt_sum = 0 
    rtt_min = float('inf') # Set an initial high value to track the lowest RTT
    rtt_max = 0 
    total_sent = 0  
    total_received = 0 
 
    try: 
        print("Heartbeat client is running. Press Ctrl + C to stop.")
        
        while seq_number <= 10: # Limit the number of heartbeats sent to 10
            sent_time = time() # Record the current sending time to measure RTT and include in the message
            message = f"Heartbeat {seq_number} {sent_time}" 
            client_socket.sendto(message.encode(), server_address)
            print(f"Heartbeat {seq_number} sent.") # Notify the user that the Heartbeat message with the given sequence number was sent successfully.
            total_sent += 1

            # Wait for server response, Set a timeout so the client doesn't wait forever for a response
            client_socket.settimeout(1)  
            try: 
                # Wait for a response from the server
                data, _ = client_socket.recvfrom(1024)
                received_time = time()  
                rtt = received_time - sent_time  
                total_received += 1  
                rtt_sum += rtt  # Add this RTT to the total for averaging later
                # Update minimum and maximum RTT based on the latest response
                rtt_min = min(rtt_min, rtt)
                rtt_max = max(rtt_max, rtt)
                
                print(f"Response from server: {data.decode()} | RTT: {rtt:.4f} seconds") # Print the server's response and RTT for debugging
            
            except timeout:
                # If no response is received within the timeout, it's considered a packet loss
                print("Request timed out.")  # Inform user of the timeout
            
            seq_number += 1 # Increment the sequence number and wait before sending the next heartbeat

            sleep(random.uniform(1, 5)) # Introduce a random delay between heartbeats to simulate real-world conditions, # Random interval between 1 and 5 seconds
        
    except KeyboardInterrupt:
        print("Shutting down client.")
    
    finally:
        # <Calculate and print summary statistics after the client stops>

        if total_received > 0: # avoid error (division by zero)
            rtt_avg = rtt_sum / total_received # Calculate average RTT if any response was received.
        else:
            rtt_avg = 0  
        
        packet_loss = ((total_sent - total_received) / total_sent) * 100

        print("\n--- Heartbeat Statistics ---")
        print(f"Packets Sent: {total_sent}")
        print(f"Packets Received: {total_received}") 
        print(f"Packet Loss: {packet_loss:.2f}%")
        print(f"RTT (min/avg/max): {rtt_min:.4f}/{rtt_avg:.4f}/{rtt_max:.4f} seconds")

        # Close the socket to release resources
        client_socket.close()
        print("Socket closed.")

if __name__ == "__main__":
    heartbeat_udpclient()
