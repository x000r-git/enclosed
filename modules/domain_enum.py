"""
Module "Domain Enumeration" for "enclosed" framework
"""

import json
import socket
from urllib.request import urlopen
from modules.generate_output_format import create_header

def information_from_crtsh(arg_list):
    """
    Exporting information from crt.sh
    :param arg_list: namespace of command line arguments
    :return: sorted list of found subdomains
    """
    domains = set()
    json_with_result = json.loads(urlopen("https://crt.sh/?q={}&output=json".format(arg_list.domain)).read().decode())
    for row in json_with_result:
        if row["name_value"][-len(arg_list.domain)-1:] == "." + arg_list.domain and "\n" not in row["name_value"]: domains.add(row["name_value"])

    return sorted(domains)

def bruteforce_subdomains(arg_list):
    """
    Brute force of subdomains
    :param arg_list: namespace of command line arguments
    :return: formatted list of found subdomains
    """
    result = "\nBruteforced and available domains:\n"
    target_domain = arg_list.domain

    if arg_list.brute_list:
        pref_list = arg_list.brute_list
    else:
        pref_list = "wordlists/default_subdomains.txt"

    with open(pref_list) as wordlist:
        while True:
            subdomain = wordlist.readline().strip()
            if not subdomain:
                break
            scheme = "{0}.{1}".format(subdomain, target_domain)

            try:
                socket.gethostbyname(scheme)
                for port in [21, 22, 80, 443, 3000, 8000, 8080]:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    if sock.connect_ex((scheme, port)) == 0:
                        result += "{0}.{1}\n".format(subdomain, target_domain)
                        break
                    sock.close()
            except Exception as e:
                # Exception raises only if no ip-addr matched with domain
                print(e)

    return result


def main(args, custom_args):
    """
    Main function of this module
    :param args: namespace of command line arguments
    :param custom_args: custom arguments that can be specified with a "-ca" flag
    :return: the output of this module
    """
    result = create_header("Domain Enumeration", "Subdomain search module", "Args: --type, --domain")

    result += "\n".join(information_from_crtsh(args))

    if args.type == "active":
        result += bruteforce_subdomains(args)

    return result + "\n"