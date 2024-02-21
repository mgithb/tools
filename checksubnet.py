#!/usr/bin/env python3

import ipaddress
import sys
from termcolor import colored  # Ensure the termcolor module is installed

def enumerate_ips(cidr):
    return [str(ip) for ip in ipaddress.IPv4Network(cidr, strict=False)]

def check_inclusion(cidr, ip):
    return ipaddress.ip_address(ip) in ipaddress.IPv4Network(cidr, strict=False)

def print_close_ips(ip_list, target_ip, num_before=2, num_after=2):
    try:
        target_index = ip_list.index(target_ip)
        start_index = max(0, target_index - num_before)
        end_index = min(len(ip_list), target_index + num_after + 1)
        for ip in ip_list[start_index:end_index]:
            print(colored(f"-> {ip}", 'yellow') if ip == target_ip else ip)
    except ValueError:
        print(f"{target_ip} is NOT in the list")

def mask_explanation(cidr):
    mask = int(cidr.split("/")[1])
    total_ips = 2 ** (32 - mask)
    usable_ips = total_ips - 2 if mask <= 30 else total_ips
    return f"Mask /{mask}: Allocates {usable_ips} usable IPs out of {total_ips} total IPs."

def validate_cidr(cidr):
    try:
        net = ipaddress.IPv4Network(cidr, strict=True)
        return True
    except ipaddress.AddressValueError:
        return False
    except ValueError as ve:
        print(f"Validation Error: {str(ve)}")
        return False

def simple_analysis(network):
    print(f"\nNetwork Address: {network.network_address}")
    print(f"Broadcast Address: {network.broadcast_address}")
    print(mask_explanation(str(network)))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./checksubnet.py <CIDR> <IP>")
        sys.exit(1)

    cidr = sys.argv[1]
    ip = sys.argv[2]

    # Validate CIDR
    if not validate_cidr(cidr):
        print(colored("Invalid CIDR notation. Please ensure it strictly follows rules.", 'red'))
        sys.exit(1)

    ip_list = enumerate_ips(cidr)
    print("\nEnumerating IPs for:", cidr)
    # Extracting the first and last IPs from the list

    first_ip, last_ip = ip_list[0], ip_list[-1]
    print(f"\nEnumerating IPs for: {cidr}")
    print(f"First IP: {first_ip}, Last IP: {last_ip}")

    print_close_ips(ip_list, ip)

    inclusion_status = check_inclusion(cidr, ip)
    inclusion_output = f"The IP {ip} IS included in {cidr}." if inclusion_status else f"The IP {ip} is NOT included in {cidr}."
    print(colored(f"\n{inclusion_output}", 'green' if inclusion_status else 'red'))

    network = ipaddress.IPv4Network(cidr, strict=False)
    simple_analysis(network)
