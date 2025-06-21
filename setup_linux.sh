#!/bin/bash

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
║         InstaForce Suite (IFS) Linux Installer         ║
╚═════════════════════════════════════════════════════════╝
${RESET}"
}

print_header

echo -e "${CYAN}${BOLD}[1]${RESET} Updating system packages..."
(sudo apt update -y &> /dev/null && sudo apt upgrade -y &> /dev/null) & show_spinner "System update"

echo -e "${CYAN}${BOLD}[2]${RESET} Installing Python 3 and pip..."
(sudo apt install python3 python3-pip -y &> /dev/null) & show_spinner "Python3 & pip"

echo -e "${CYAN}${BOLD}[3]${RESET} Installing Python modules: instagrapi, cryptography, colorama..."
(pip3 install --upgrade pip &> /dev/null && pip3 install instagrapi cryptography colorama &> /dev/null) & show_spinner "Python modules"

echo -e "${CYAN}${BOLD}[4]${RESET} Installing banner/terminal dependencies: figlet, toilet, boxes, cowsay, ruby..."
(sudo apt install figlet toilet boxes cowsay ruby -y &> /dev/null) & show_spinner "Banner tools"

echo -e "${CYAN}${BOLD}[5]${RESET} Installing lolcat (via gem)..."
(sudo gem install lolcat &> /dev/null) & show_spinner "lolcat"

echo -e "${GREEN}${BOLD}All dependencies installed successfully!${RESET}"
echo
echo -e "${YELLOW}${BOLD}Tip:${RESET} You can customize your banner in ${CYAN}banner.txt${RESET}."
echo -e "${CYAN}${BOLD}Run with:${RESET} python3 instaforce_suite.py"
