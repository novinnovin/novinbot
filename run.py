import os
import subprocess
import sys

# Function to check and install requirements
def ensure_requirements_installed():
    requirements = [
        "python-telegram-bot==13.15",
        "telethon",
        "jdatetime",
        "pymysql",
        "requests",
        "psutil",
        "termcolor",
    ]

    for package in requirements:
        try:
            # Check if the package is already installed
            __import__(package.split("==")[0])
        except ImportError:
            # Install the package if not installed
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    os.system('clear')

# Upgrade pip
print("Upgrading pip...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

# Ensure requirements are installed
ensure_requirements_installed()

# Your existing code starts here
import signal
import utility as utl
from colorama import init, Fore, Style
from termcolor import colored
from itertools import cycle

# Initialize colorama
init()

# ASCII art menu with rainbow effect
def print_menu():
    ascii_art = """
  _  _         _      ___  ___ _____   | Thu Feb 13 02:23:55 PM UTC 2025
 | \| |_____ _(_)_ _ | _ )/ _ \_   _|  | github.com/BDadmehr0
 | .` / _ \ V / | ' \| _ \ (_) || |    |
 |_|\_\___/\_/|_|_||_|___/\___/ |_|    | v.1
                                     
    """
    rainbow_colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA])
    for line in ascii_art.splitlines():
        print(next(rainbow_colors) + line + Style.RESET_ALL)

# Get the current script's directory and filename
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.basename(__file__)

# Kill any existing processes running this script
utl.get_params_pids_by_full_script_name(script_names=[f"{directory}/{filename}"], is_kill_proccess=True)

# List of scripts to run as subprocesses
scripts_to_run = ["bot.py", "cron_settings.py", "cron_operation.py"]

# Store active subprocesses
processes = []

# Print the menu
print_menu()

# Start each script in a separate process
for script in scripts_to_run:
    script_path = os.path.join(directory, script)
    if os.name == "nt":  # For Windows
        process = subprocess.Popen(
            [utl.python_version, script_path],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:  # For Unix-based systems
        process = subprocess.Popen(
            [utl.python_version, script_path],
            preexec_fn=os.setsid
        )
    processes.append(process)

# Monitor processes and handle keyboard interruption
try:
    print(colored("Press Ctrl+C to stop all processes.", "green"))
    while True:
        pass  # Keep the main process running
except KeyboardInterrupt:
    print(colored("\nStopping all processes...", "red"))
    for process in processes:
        try:
            if os.name == "nt":  # For Windows
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(process.pid)])
            else:  # For Unix-based systems
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception as e:
            print(colored(f"Error stopping process {process.pid}: {e}", "yellow"))
