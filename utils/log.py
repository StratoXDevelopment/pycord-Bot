from .color import colorize
from .banner import print_banner

def gray(value: bool):
    if value:
        return colorize("[", fg="gray", bold=False)
    else:
        return colorize("]", fg="gray", bold=False)
    
def colored(color, text, bold: bool = False):
    return f"{gray(True)}{colorize(text, fg=color, bold=bold)}{gray(False)}"

def error(text: str):
    print(colored("red", "ERROR", True), text)
    raise text

def success(text: str):
    print(colored("green", "SUCCESS", True), text)

def warn(text: str):
    print(colored("yellow", "WARNING", True), text)

def info(text: str):
    print(colored("blue", "INFO", True), text)

def banner():
    print_banner()
