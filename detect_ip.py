import socket
import ipaddress

def is_ip_used(ip,port):
    # Check if the IP address is in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((ip, int(port)))
    sock.close()
    return result == 0

def print_ips():
    # Define the IP range to check
    start_ip = '192.168.0.1'
    end_ip = '192.168.0.255'

    # ANSI escape sequences for text color
    red = "\u001b[31m"
    green = "\u001b[32m"
    reset = "\u001b[0m"

    # Iterate through the IP range and print used and unused IPs with color
    current_ip = ipaddress.IPv4Address(start_ip)
    answer = input("port> ")

    while str(current_ip) != end_ip:
        ip_str = str(current_ip)
        if is_ip_used(ip_str, answer):
            print(f"{red}Used:\t{ip_str}:{answer}{reset}")
        else:
            print(f"{green}Unused:\t{ip_str}:{answer}{reset}")
        current_ip = current_ip + 1

print_ips()