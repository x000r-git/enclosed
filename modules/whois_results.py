"""
Module "WHOIS Results" for "enclosed" framework
"""

import json
from urllib.request import urlopen
from modules.generate_output_format import create_header

def filter_response(json_string_response):
    """
    Extracting information from whois
    :param json_string_response: string with json
    :return: information from whois
    """
    try:
        response_json = json.loads(json_string_response.read().decode())
        return response_json["whois"]
    except:
        return "Got an error. Try to recheck your CLI arguments..."

def main(args, custom_args):
    """
    Main function of this module
    :param args: namespace of command line arguments
    :param custom_args: custom arguments that can be specified with a "-ca" flag
    :return: the output of this module
    """
    result = create_header("WHOIS Results", "Extract information from WHOIS", "Args: --domain, --ip")

    try:
        if args.domain:
            result += "Domain information:\n" + filter_response(urlopen("http://api.whois.vu/?clean&q=" + args.domain))
        if args.ip:
            result += "\nIP information:\n" + filter_response(urlopen("http://api.whois.vu/?s=ip&clean&q=" + args.ip))

    except:
        result += "Something went wrong, sorry, try to debug this module"

    return result + "\n"*2