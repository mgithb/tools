#!/usr/bin/env python3

import sys
import base64
import urllib.parse

def decode_base64(data):
    return base64.b64decode(data).decode('utf-8')

def encode_base64(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def decode_url(data):
    return urllib.parse.unquote(data)

def encode_url(data):
    return urllib.parse.quote(data)

def decode_bytecode(data):
    try:
        decoded_str = bytes.fromhex(data.replace("\\x", "")).decode('utf-8', 'replace')
        return decoded_str
    except ValueError:
        return "Invalid bytecode format"

def decode_php_hex(data):
    try:
        # Removing unwanted characters and decoding
        cleaned_data = data.replace('<?php', '').replace('/*', '').replace('*/', '').replace(' ', '')
        decoded_str = bytes.fromhex(cleaned_data).decode('utf-8', 'replace')
        return decoded_str
    except ValueError:
        return "Invalid PHP hex format"

def print_help():
    print('''Usage: decoder.py [method] <data>

Methods:
    b64      - Base64 decode
    b64e     - Base64 encode
    url      - URL decode
    urle     - URL encode
    byte     - Byte decode
    phphex   - PHP Hex decode
    help     - Show this help menu
    ''')

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    method = sys.argv[1]

    if method == "help":
        print_help()
        sys.exit(0)

    if len(sys.argv) < 3:
        data = input("Enter the data: ")
    else:
        data = sys.argv[2]

    if method == "b64":
        print(decode_base64(data))
    elif method == "b64e":
        print(encode_base64(data))
    elif method == "url":
        print(decode_url(data))
    elif method == "urle":
        print(encode_url(data))
    elif method == "byte":
        print(decode_bytecode(data))
    elif method == "phphex":
        print(decode_php_hex(data))
    else:
        print(f"Unknown method: {method}")
        sys.exit(1)

if __name__ == "__main__":
    main()
