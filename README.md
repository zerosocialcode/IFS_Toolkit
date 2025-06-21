# InstaForce Suite (IFS)

A powerful, professional, and user-friendly Instagram authentication penetration toolkit.

**Developer:** [zerosocialcode](https://github.com/zerosocialcode)  
**Repository:** [IFS-InstaForce-Suite](https://github.com/zerosocialcode/IFS_Toolkit)

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [APIs and Libraries Used](#apis-and-libraries-used)
- [Installation](#installation)
- [Proxy Validation](#proxy-validation)
- [Usage](#usage)
- [Banner Customization](#banner-customization)
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
- **Banner Customization**  
  *Prints ASCII or Unicode banners from `banner.txt` exactly as pasted, with no formatting issues.*
- **Failure Logging & Reporting**  
  *Logs all failed attempts (password masked) and technical logs; session summary at the end.*
- **Cross-Terminal Compatibility**  
  *Works on Linux, Termux/Android, cloud shells, and more. No shelling out or escape errors.*
- **Automatic Proxy Banning**  
  *Detects and removes proxies that get rate-limited or banned during attacks.*
- **Professional, Colorized Terminal Output**  
  *Easy-to-read, color-coded console feedback for all status messages.*

---

## How It Works

1. **Banner & Legal Warning**:  
   Prints your custom banner (`banner.txt`) and a legal warning.
2. **User Input**:  
   Prompts for Instagram username, password list, and (optionally) a validated proxy list.
3. **Session Handling**:  
   Loads session if available and encrypted, or creates new.
4. **Attack Execution**:  
   - If proxies are supplied: runs multiple parallel login attempts, each using a different proxy, with a live spinner showing progress.
   - If no proxies: runs login attempts serially.
   - Each password attempt randomly delays (configurable) to avoid rate-limiting and detection.
5. **Result Logging**:  
   - Successful credentials saved encrypted for future use.
   - Failed attempts are masked and logged.
   - Banned/rate-limited proxies are detected and not reused.
   - At end, prints a colorized session summary.
6. **No OTP/2FA Handling**:  
   If Instagram requests OTP or 2FA, the script logs and skips the attempt (no prompt for code).

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

1. **Prepare your files:**
    - `banner.txt`: Any ASCII/Unicode art or text banner you want.
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

## Banner Customization

- Paste any text, ASCII, or Unicode art into `banner.txt`.
- The script prints it exactly as-is, supporting all formatting and characters.
- No need for external tools or escaping.

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

## Credits

- **Developer:** [zerosocialcode](https://github.com/zerosocialcode)
- **instagrapi:** Instagram private API library by [adw0rd](https://github.com/adw0rd/instagrapi)

---

**For educational and authorized testing only. Respect privacy and the law.**
