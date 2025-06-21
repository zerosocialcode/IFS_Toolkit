#!/usr/bin/env python3
"""
Proxy Validator for IFS-InstaForce-Suite

Checks which proxies can reach Instagram's login page.

Usage:
    python3 proxy_validator.py proxies.txt

- proxies.txt: File with one proxy per line. (http[s]://ip:port or socks5://user:pass@ip:port)

Results:
    - valid_proxies.txt      (Proxies that succeeded)
    - invalid_proxies.txt    (Proxies that failed)
    - usetheseproxy.txt      (Same as valid_proxies.txt; for use in main suite)

Developer: zerosocialcode
GitHub: https://github.com/falconthehunter
"""

import sys
import requests
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)

DEST_URL = "https://www.instagram.com/accounts/login/"
TIMEOUT = 8

# Colors
CYAN = Fore.CYAN + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
RED = Fore.RED + Style.BRIGHT
RESET = Style.RESET_ALL

def print_header():
    print(f"""{CYAN}
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘           Proxy Validator for IFS           â•‘
â•‘   Developer: zerosocialcode                 â•‘
â•‘   GitHub: https://github.com/falconthehunterâ•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
{RESET}""")

def load_proxies(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[!] Failed to load proxy file: {e}{RESET}")
        sys.exit(1)

class Spinner:
    spinner_cycle = ['|', '/', '-', '\\']
    def __init__(self, message):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.spin)
        self.idx = 0
        self.message = message

    def spin(self):
        while not self.stop_event.is_set():
            spin_char = self.spinner_cycle[self.idx % len(self.spinner_cycle)]
            print(f"\r{CYAN}{self.message} {spin_char}{RESET}", end='', flush=True)
            self.idx += 1
            time.sleep(0.13)
        print("\r" + " " * (len(self.message) + 4) + "\r", end='', flush=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

def check_proxy(proxy):
    proxies = {"http": proxy, "https": proxy}
    try:
        r = requests.get(DEST_URL, proxies=proxies, timeout=TIMEOUT)
        if 200 <= r.status_code < 400:
            return True
    except Exception:
        pass
    return False

def main():
    print_header()
    if len(sys.argv) != 2:
        print(f"{CYAN}Usage:{RESET} python3 proxy_validator.py proxies.txt")
        sys.exit(1)
    proxy_file = sys.argv[1]
    proxies = load_proxies(proxy_file)
    if not proxies:
        print(f"{RED}[!] No proxies found in {proxy_file}{RESET}")
        sys.exit(1)
    print(f"{CYAN}Loaded {len(proxies)} proxies. Testing against:{RESET} {DEST_URL}\n")

    valid, invalid = [], []

    try:
        for idx, proxy in enumerate(proxies, 1):
            msg = f"Checking if proxy is valid ({idx}/{len(proxies)})"
            spinner = Spinner(msg)
            spinner.start()
            is_valid = check_proxy(proxy)
            spinner.stop()
            if is_valid:
                print(f"{GREEN}[VALID]{RESET} {proxy}")
                valid.append(proxy)
            else:
                print(f"{RED}[INVALID]{RESET} {proxy}")
                invalid.append(proxy)
    except KeyboardInterrupt:
        print(f"\n{CYAN}Gracefully exiting...{RESET}")
        pass

    # Save valid proxies to three files: valid_proxies.txt, usetheseproxy.txt, and invalid_proxies.txt
    with open("valid_proxies.txt", "w", encoding="utf-8") as f:
        for p in valid:
            f.write(p + "\n")
    with open("usetheseproxy.txt", "w", encoding="utf-8") as f:
        for p in valid:
            f.write(p + "\n")
    with open("invalid_proxies.txt", "w", encoding="utf-8") as f:
        for p in invalid:
            f.write(p + "\n")

    print(f"\n{CYAN}Finished!{RESET} {GREEN}{len(valid)} valid{RESET}, {RED}{len(invalid)} invalid{RESET} proxies.")
    print(f"{CYAN}Saved valid proxies to valid_proxies.txt and usetheseproxy.txt")
    print(f"Saved invalid proxies to invalid_proxies.txt{RESET}")

if __name__ == "__main__":
    main()