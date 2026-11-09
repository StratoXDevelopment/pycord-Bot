R      = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
MAG    = "\033[95m"

ART = [
    "██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗ ",
    "██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗",
    "██║ █╗ ██║███████║   ██║   ██║     ███████║█████╗  ██████╔╝",
    "██║███╗██║██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗",
    "╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║",
    " ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
]

INFO = [
    ("Version", GREEN,  "1.0.0"),
    ("Prefix ", YELLOW, "!"),
    ("Python ", CYAN,   "3.14"),
    ("Library", MAG,    "Pycord"),
]

def print_banner():
    W = 62
    print()
    for line in ART:
        print(f"  {RED}{BOLD}{line}{R}")
    print()
    print(f"  {DIM}{'─' * W}{R}")
    for label, color, value in INFO:
        print(f"  {DIM}{label}{R}  {BOLD}{color}{value}{R}")
    print(f"  {DIM}{'─' * W}{R}")
