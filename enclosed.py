import os
import json
import argparse
import importlib


def get_input_information():
    """
    Getting command line arguments
    :return: namespace of command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="Type of scanning [active/passive]", required=True)
    parser.add_argument("-d", "--domain", help="Domain", required=True)
    parser.add_argument("-i", "--ip", help="IP")
    parser.add_argument("-l", "--brute_list", help="Brute list for subdomain finder module")
    parser.add_argument("-ca", "--custom_args", help="Provide arguments for custom modules")
    parser.add_argument("-cm", "--custom_modules", help="List of custom_modules")
    return parser.parse_args()

def module_from_file(module_name, file_path):
    """
    Provides access to the module by name. Part of the code is taken from shorturl.at/csB28
    :param module_name: the name of the module to access
    :param file_path: the path where the module is located
    :return: the module, as if the import function was launched
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_output_file(arg_list):
    """
    Initialization of the file where the output will be saved
    :param arg_list: namespace of command line arguments
    :return: the name of the file where the output is saved
    """
    filename = arg_list.domain + ".result"
    with open(filename, "w") as f:
        f.write("# enclosed output file #\n")
    return filename

def output_to_file(result, arg_list):
    """
    Top up the output file with the result
    :param result: data to be added to the file
    :param arg_list: namespace of command line arguments
    :return: None
    """
    filename = arg_list.domain + ".result"
    with open(filename, "a") as f:
        f.write("\n" + result + "\n")

def module_run(name, args, custom_args):
    """
    Function that launches a module by its name with arguments
    :param name: module name
    :param args: namespace of command line arguments
    :param custom_args: custom arguments that can be specified with a "-ca" flag
    :return: output of the module if it has completed successfully, otherwise an error message is returned
    """
    try:
        return module_from_file(name, "{0}/modules/{1}.py".format(os.getcwd(), name)).main(args, custom_args)
    except Exception as e:
        return "Module {0} error".format(name)

def load_configuration():
    """
    Reading the "enclosed" configuration from .config.json
    :return: list of modules for active and passive scanning
    """
    with open(".config.json") as config_file:
        config = json.loads(config_file.read())
        return [config["active"], config["passive"]]

def run_scan(arg_list, custom_arg_list, modules):
    """
    Function that starts scanning the target
    :param arg_list: namespace of command line arguments
    :param custom_arg_list: custom arguments that can be specified with a "-ca" flag
    :param modules: configuration from the .config.json file
    :return: None
    """
    if arg_list.type == "active":
        modules = modules[0]
    else:
        modules = modules[1]

    try:
        modules += [custom_module.strip() for custom_module in arg_list.custom_modules.split(",")]
    except AttributeError:
        # no custom modules provided
        pass

    for module in modules:
        output_to_file(str(module_run(module, arg_list, custom_arg_list)), arg_list)
        print("{0} module execution completed".format(module))

def main():
    """
    Main function of the "enclosed"
    :return: None
    """
    arg_list = get_input_information()
    try:
        custom_arg_list = [i.strip() for i in arg_list.custom_args.split(",")]
    except AttributeError:
        custom_arg_list = []

    create_output_file(arg_list)
    run_scan(arg_list, custom_arg_list, load_configuration())


if __name__ == "__main__":
    main()