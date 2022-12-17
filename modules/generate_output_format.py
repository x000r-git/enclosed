def create_header(module_name = "test_module", module_descr = "it doesn't do anything", module_input="it needs three arguments: name, surname, weight"):
    """
    Function that generates a header for any "enclosed" module
    :param module_name:
    :param module_descr:
    :param module_input:
    :return: the header for any module
    """
    property_set = (module_name, module_descr, module_input)
    mult = max([len(prop) for prop in property_set]) + 4

    header = "*"*mult + "\n"
    for prop in property_set:
        header += "* " + prop + " " * (mult - 4 - len(prop)) + " *\n"
    header += "*"*mult + "\n"

    return header