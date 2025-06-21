#!/data/data/com.termux/files/usr/bin/bash

CYAN='\033[96m'
GREEN='\033[92m'
RED='\033[91m'
YELLOW='\033[93m'
BOLD='\033[1m'
RESET='\033[0m'

show_spinner() {
    local pid=$!
    local spin='-\|/'
    local i=0
    tput civis
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) %4 ))
        printf "\r${CYAN}${BOLD}[*] $1... ${spin:$i:1} ${RESET}"
        sleep .2
    done
    printf "\r${GREEN}${BOLD}[✓] $1                     ${RESET}\n"
    tput cnorm
}

print_header() {
echo -e "${CYAN}${BOLD}
╔═════════════════════════════════════════════════════════╗
║        InstaForce Suite (IFS) Termux Installer         ║
╚═════════════════════════════════════════════════════════╝
${RESET}"
}

print_header

echo -e "${CYAN}${BOLD}[1]${RESET} Updating system packages..."
(pkg update -y &> /dev/null && pkg upgrade -y &> /dev/null) & show_spinner "System update"

echo -e "${CYAN}${BOLD}[2]${RESET} Installing Python and pip..."
(pkg install python -y &> /dev/null) & show_spinner "Python & pip"

echo -e "${CYAN}${BOLD}[3]${RESET} Installing Python modules: instagrapi, cryptography, colorama..."
(pip install --upgrade pip &> /dev/null && pip install instagrapi cryptography colorama &> /dev/null) & show_spinner "Python modules"

echo -e "${CYAN}${BOLD}[4]${RESET} Installing terminal dependencies: figlet, toilet, boxes, cowsay..."
(pkg install figlet toilet boxes cowsay -y &> /dev/null) & show_spinner "Banner tools"

echo -e "${CYAN}${BOLD}[5]${RESET} Installing lolcat (via gem)..."
(gem install lolcat &> /dev/null) & show_spinner "lolcat"

echo -e "${GREEN}${BOLD}All dependencies installed successfully!${RESET}"
echo
echo -e "${YELLOW}${BOLD}Tip:${RESET} You can customize your banner in ${CYAN}banner.txt${RESET}."
echo -e "${CYAN}${BOLD}Run with:${RESET} python instaforce_suite.py"
