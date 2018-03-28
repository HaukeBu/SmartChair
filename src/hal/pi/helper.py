import re

def uppercase_to_camelcase(text):
    temp = text.lower().split('_')

    return temp[0] + "".join(map(str.capitalize, temp[1:]))


def camelcase_to_uppercase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

def list_to_json_string(lst):
    ret_str = '{"values": ['

    for idx in range(len(lst)):
        ret_str += '{"id": ' + str(idx) + ', "value": ' + str(lst[idx]) + '}'

        if idx < len(lst) - 1:
            ret_str += ', '

    ret_str += ']}'

    return ret_str
