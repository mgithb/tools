import requests
import socket
from ipwhois import IPWhois
import ipcalc
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor

def get_ptr_and_netname(item):
    try:
        # Initial setup for timeout
        socket.setdefaulttimeout(0.5)
        first_ip = item  # Use the original item for processing

        # If item is a subnet, we only use the first IP for DNS and WHOIS queries
        if '/' in item:
            subnet = ipcalc.Network(item)
            first_ip = str(subnet.host_first())

        # Attempt DNS resolution
        resolved_data = None
        try:
            resolved_data = socket.gethostbyaddr(first_ip)[0]
        except socket.herror:
            pass  # DNS resolution failed, continue to WHOIS

        # Attempt WHOIS lookup if DNS resolution fails
        if not resolved_data:
            try:
                obj = IPWhois(first_ip)
                whois_result = obj.lookup_rdap(depth=1)
                netname = whois_result['network']['name']
                handle = whois_result['network']['handle']
                asn_description = whois_result.get('asn_description', 'None')
                resolved_data = f"NetName: {netname}, {asn_description}, {handle}"
            except Exception as e:
                resolved_data = f"WHOIS error: {str(e)}"

        return f"{item} : {resolved_data}"
    except Exception as e:
        return f"Error: {str(e)}"

def process_ips_or_subnets(file_or_url):
    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))
        
        # Read IPs or subnets
        if file_or_url.startswith('http'):
            response = session.get(file_or_url)
            ips_or_subnets = response.text.splitlines()
        else:
            with open(file_or_url, 'r') as file:
                ips_or_subnets = file.read().splitlines()

        # Remove comments and empty lines
        ips_or_subnets = [line.strip() for line in ips_or_subnets if line.strip() and not line.strip().startswith('#')]

        # Process each IP or subnet in parallel (without RoundRobin)
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(get_ptr_and_netname, ip) for ip in ips_or_subnets]
            for future in futures:
                result = future.result()
                print(result)  # Print each result as it completes
                results.append(result)

        return results
    except Exception as e:
        return str(e)

# Usage
#file_or_url = 'https://files.imunify360.com/static/whitelist/v2/google.txt'
#results = process_ips_or_subnets(file_or_url)

# Usage example
file_or_url = 'http://192.168.21.100:8000/google.txt'
results = process_ips_or_subnets(file_or_url)
