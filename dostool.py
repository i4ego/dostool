import sys
import re

SUPPORTED_ACTIONS = ("tcp", "udp", "http")
IP_PATTERN = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([1-9]\d*|0)$'
DOMAIN_PATTERN = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}:([1-9]\d*|0)$'

def help(msg: str = ""):
    print(msg)

def parse_argv(argv: list) -> tuple[str, list[tuple[str, int]]]:
    if len(argv) <3:
        help()
        return
    if argv[1] == "help":
        help()
        return
    argv = argv[1:]

    action = argv[0]
    if action not in SUPPORTED_ACTIONS:
        help(f"Unknown action: {action}!")
        return
    
    r_targets = argv[1:]
    targets = list()
    for target in r_targets:
        if re.match(IP_PATTERN, target):
            pass
        elif re.match(DOMAIN_PATTERN, target):
            pass
        else:
            help("Invalid IP / domain!")
            return
        targets.append((target.split(":")[0], int(target.split(":")[1])))
    return action, targets

if __name__ == "__main__":
    print(parse_argv(sys.argv))