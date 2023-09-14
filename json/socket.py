import socket
import os

# Snort IP address and port
snort_ip = "192.168.56.8"  # Replace with Snort's IP address
snort_port = 514    # Replace with Snort's port number

# Named pipe path
pipe_path = "home/janith/path/snort_pipe"  # Replace with the actual path

# Check if the named pipe exists
if not os.path.exists(pipe_path):
    print(f"The named pipe '{pipe_path}' does not exist.")
else:
    try:
        # Create a socket connection to Snort
        snort_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        snort_socket.connect((snort_ip, snort_port))

        # Read data from the named pipe and send it to Snort
        with open(pipe_path, "r") as pipe:
            while True:
                data = pipe.read(4096)
                if not data:
                    break
                snort_socket.send(data.encode())

        # Close the socket
        snort_socket.close()
        print("Data sent to Snort successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
