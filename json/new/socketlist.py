import socket

# Snort machine address and port
snort_machine_ip = "0.0.0.0"  # Listen on all available interfaces
snort_machine_port = 12345  # Use the same port as in the sender script

# Create a socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as snort_server:
    snort_server.bind((snort_machine_ip, snort_machine_port))
    snort_server.listen()

    print("Snort server is listening...")

    while True:
        connection, client_address = snort_server.accept()
        with connection:
            print("Connected to:", client_address)
            data = connection.recv(1024).decode("utf-8")
            print("Received data:\n", data)

            # Add your Snort rule detection logic here
            if "urgent" in data or "important" in data or "free giveaway" in data:
                print("Suspicious email detected!")
