# InstaForce Suite (IFS)

A powerful, professional, and user-friendly Instagram authentication penetration toolkit.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [APIs and Libraries Used](#apis-and-libraries-used)
- [Installation](#installation)
- [Proxy Validation](#proxy-validation)
- [Usage](#usage)
- [Session & Security](#session--security)
- [Legal & Disclaimer](#legal--disclaimer)

---

## Features

- **Parallel and Serial Attack Modes**  
  *Uses proxies for high-speed, parallel brute-forcing, or serial mode if no proxies provided.*
- **Live Job Spinner and Status**  
  *Displays a single spinner with dynamic progress and job count during attacks.*
- **Session Management**  
  *Automatically saves, loads, and encrypts session data for each username, minimizing lockouts and relogins.*
- **Full Proxy Support & Validation**  
  *Supports HTTP, HTTPS, SOCKS5 proxies; includes a dedicated proxy validator to filter working proxies before attacks.*
- **Failure Logging & Reporting**  
  *Logs all failed attempts (password masked) and technical logs; session summary at the end.*
- **Cross-Terminal Compatibility**  
  *Works on Linux, Termux/Android, cloud shells, and more. No shelling out or escape errors.*
- **Automatic Proxy Banning**  
  *Detects and removes proxies that get rate-limited or banned during attacks.*
- **Professional, Colorized Terminal Output**  
  *Easy-to-read, color-coded console feedback for all status messages.*

---

## APIs and Libraries Used

- **[instagrapi](https://github.com/adw0rd/instagrapi)**  
  - Used as the main Instagram private API client for authentication and session handling.
- **[cryptography](https://cryptography.io/)**  
  - Used for AES/Fernet encryption of session files for security.
- **[colorama](https://pypi.org/project/colorama/)**  
  - Used for cross-platform colorized terminal output (proxy_validator.py).
- **Python Standard Library**
  - `threading`, `concurrent.futures`, `queue`, `logging`, `random`, and more for concurrency, UI, and file operations.

---

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/zerosocialcode/IFS_Toolkit.git
cd IFS-Toolkit
```

### 2. Install Dependencies

#### For Linux

```sh
bash setup_linux.sh
```
*Installs: Python3, pip, `instagrapi`, `cryptography`, `colorama`, and optional banner tools (`figlet`, `toilet`, etc.).*

#### For Termux/Android

```sh
bash setup_termux.sh
```
*Installs: Python, pip, and all required Python modules for Android/Termux.*

Or, manually install with pip:

```sh
pip3 install instagrapi cryptography colorama
```

---

## Proxy Validation

**Before running the attack, always validate your proxies!**

1. Place your proxies (one per line) in `proxies.txt`.
2. Run the validator:

    ```sh
    python3 proxy_validator.py proxies.txt
    ```

3. Working proxies are saved to `usetheseproxy.txt` for use in the main suite.  
   Dead proxies go to `invalid_proxies.txt`.

---

## Usage

1. **Keep you wordlist in a file.**
    - `passwords.txt`: One password per line.
    - `usetheseproxy.txt`: Validated proxies from the validator (optional).

2. **Run the main suite:**

    ```sh
    python3 instaforce-suite.py
    ```

3. **Follow prompts:**
    - Instagram username
    - Path to password list (e.g., `passwords.txt`)
    - Path to proxy list (`usetheseproxy.txt` or leave blank for no proxies)

4. **Review results:**
    - Session summary and unlocked accounts shown at the end.
    - Failed attempts in `ifs_failed.log`
    - Technical logs in `ifs_session.log`

---

## Session & Security

- **Sessions are encrypted** with Fernet/AES and stored in `ifs_sessions/`.
- **No passwords or session data are stored in plaintext.**
- **Failed attempts** are logged with masked passwords.

---

## Legal & Disclaimer

> ⚠️ **WARNING:**  
> Use this tool at your own risk.  
> You are responsible for your actions.  
> The author assumes no liability for misuse or illegal activity.

---
**For educational and authorized testing only. Respect privacy and the law.**
