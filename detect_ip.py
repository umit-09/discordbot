import socket

def is_ip_used(ip):
    # Check if the IP address is in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip, 22))  # Test SSH port 22
    sock.close()
    return result == 0

def print_unused_ips():
    # Define the IP range to check
    start_ip = '192.168.0.1'
    end_ip = '192.168.0.255'

    # Iterate through the IP range and print unused IPs
    current_ip = start_ip
    while current_ip != end_ip:
        if not is_ip_used(current_ip):
            print(current_ip)
        current_ip = socket.inet_ntoa(socket.inet_aton(current_ip) + b'\x00')

print_unused_ips()