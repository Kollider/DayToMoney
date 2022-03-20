import re


def separator(original_value):
    quantity = re.findall('\d+|\d+,\d+', original_value)
    if len(quantity) > 1:
        quantity = [','.join(quantity)]
    quantity_str = '' + quantity[0]
    quantity_type = original_value.replace(quantity_str, '')

    return quantity[0], quantity_type


"""test_string = '1,93л'
a = separator(test_string)
print(a)"""
