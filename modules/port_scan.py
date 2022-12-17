"""
Module "Port Scanner" for "enclosed" framework
"""

import socket
from modules.generate_output_format import create_header

def run_port_scan(arg_list):
    """
    Launching TCP port scanning using sockets
    :param arg_list: namespace of command line arguments
    :return: sorted list of ports
    """
    open_ports = set()
    if arg_list.ip:
        target_ip = arg_list.ip
    else:
        target_ip = socket.gethostbyname(arg_list.domain)
    for port in [20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 143, 443, 3000, 3389, 8000, 8080]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((target_ip, port)) == 0:
            open_ports.add(port)
        sock.close()
    return sorted(open_ports)


def main(args, custom_args):
    """
    Main function of this module
    :param args: namespace of command line arguments
    :param custom_args: custom arguments that can be specified with a "-ca" flag
    :return: the output of this module
    """
    result = create_header("Port Scanner (TCP)", "Port scanning module", "Args: --domain, --ip (optionally)")
    result += "Open ports: " + " ".join([str(port) for port in run_port_scan(args)])

    return result + "\n"*2