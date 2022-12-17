"""
Module "Leakcheck Results" for "enclosed" framework
"""

import re
import json
import urllib.request
from modules.generate_output_format import create_header

def parse_output(data, email):
    """
    Parser for the received data. Retrieves information about the sites where leaks occurred
    :param data: string with json format
    :param email: target email
    :return: formatted list of found leaks
    """
    response_json = json.loads(data)
    total_results = response_json["found"]
    result = "\n{0} results for {1}:\n".format(total_results, email)
    for row in response_json["sources"]:
        result += "{0}\n".format(row["name"])

    return result

def main(args, custom_args):
    """
    Main function of this module
    :param args: namespace of command line arguments
    :param custom_args: custom arguments that can be specified with a "-ca" flag
    :return: the output of this module
    """
    result = create_header("Leakcheck Results", "Export results from leakcheck.io", "Args: -ca user1_email,user2_email,key:<api_key>")
    emails = []

    try:
        for arg in custom_args:
            if 'key:' in arg:
                api_key = arg[4:]
            if re.search(r'[\w.]+\@[\w.]+', arg):
                emails.append(arg)
    except:
        return result + "Error in module..."

    for email in emails:
        req = urllib.request.Request("https://leakcheck.io/api/public?key={0}&check={1}".format(api_key, email), headers={'User-Agent': "enclosed 1.0.0"})
        result += parse_output(urllib.request.urlopen(req).read().decode(), email)

    return result + "\n"*2
