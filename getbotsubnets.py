import requests
import sys
import tempfile
import os
def fetch_ip_data():
    bots_urls = {
        'google-bot': 'https://developers.google.com/static/search/apis/ipranges/googlebot.json',
        'google-special': 'https://developers.google.com/static/search/apis/ipranges/special-crawlers.json',
        'google-users': 'https://developers.google.com/static/search/apis/ipranges/user-triggered-fetchers.json',
        'bing-bot': 'https://www.bing.com/toolbox/bingbot.json'
    }
    ip_ranges = []
    for bot_name, url in bots_urls.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for prefix in data.get('prefixes', []):
                for key in ['ipv4Prefix', 'ipv6Prefix']:
                    network = prefix.get(key)
                    if network:
                        ip_ranges.append(network)
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            sys.exit(1)
        except ValueError as e:
            print(f"Error processing data from {url}: {e}")
            sys.exit(1)
    return sorted(set(ip_ranges))
def write_to_file(ip_ranges):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        for network in ip_ranges:
            tmp_file.write(f"{network}\n".encode())
    os.replace(tmp_file.name, 'bot_ip_ranges.data')
def main():
    ip_ranges = fetch_ip_data()
    write_to_file(ip_ranges)
if __name__ == "__main__":
    main()
