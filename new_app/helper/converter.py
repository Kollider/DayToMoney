def converter(test_val):  # ('1,93', 'л')
    quantity = test_val[0]
    quantity_type = test_val[1]

    if ',' in str(quantity):
        quantity = str(quantity).replace(",", ".")

    match quantity_type:
        case 'л' | 'Л':
            new_quantity = int(round(float(quantity) * 1000))
            new_quantity_type = 'мл'
            return new_quantity, new_quantity_type
        case 'кг'|'Кг'|'КГ':
            new_quantity = int(round(float(quantity) * 1000))
            new_quantity_type = 'г'
            return new_quantity, new_quantity_type
        case _:
            new_quantity = quantity
            new_quantity_type = quantity_type
            return new_quantity, new_quantity_type


"""test_conv = ('1,93', 'л')
a=converter(test_conv)
print(a)"""

# todo add map or lambda function
# map(converter, test_conv)
