import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose = False):
    has_letters = any(c.isalpha() for c in target)
    ip_address = ""
    hostname = target
    hostname_not_found = False
    error = ""

    if has_letters:
        try:
            ip_address = socket.gethostbyname(target)
        except:
            error = "Error: Invalid hostname"
    else:
        ip_address = target
        try:
            socket.inet_aton(ip_address)
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
            except:
                hostname_not_found = True
        except:
            error = "Error: Invalid IP address"
    
    if error:
        return error
    
    open_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            if sock.connect_ex((ip_address, port)) == 0:
                open_ports.append(port)
    
    if not verbose:
        return open_ports

    if hostname_not_found:
        result = f"Open ports for {ip_address}\n"
    else:
        result = f"Open ports for {hostname} ({ip_address})\n"
    
    result += "PORT     SERVICE\n"
    for port in open_ports:
        service = ports_and_services.get(port, "unknown")
        spaces = " " * (9 - len(str(port)))
        result += f"{port}{spaces}{service}\n"
    
    return result.rstrip("\n")


