# read csv file and import data to database
#    day = db.Column(db.Date, nullable=True, default=datetime.date.today)
#    name_of_item = db.Column(db.String(40), nullable=True)
#    quantity = db.Column(db.Integer, nullable=True, default=1)
#    quantity_type = db.Column(db.String(5), nullable=True, default='it')
#    spending_amount = db.Column(db.Integer, nullable=True)
#
#    user_id = db.Column(db.Integer, db.ForeignKey('usert.id'), nullable=True)

# todo implement user_id, output_to_csv

import pandas as pd
from datetime import datetime

from app import Spendings, db
from app.helper.converter import converter
from app.helper.separator import separator

filename = 'files/Finances.csv'
df = pd.read_csv(filename, encoding='windows-1251', sep=';')

day = ''

for index, row in df.iterrows():
    # print(row)

    day_value = row['day']
    name_of_item = row['name']

    quantity_value = row['quantity']
    quantity = ''
    quantity_type = ''

    spending_amount = row['price']

    if pd.isnull(day_value):
        if pd.isnull(quantity_value):
            pass
        else:
            separated = separator(quantity_value)
            converted = converter(separated)
            converted_quantity = converted[0]
            converted_quantity_type = converted[1]
            quantity = converted_quantity
            quantity_type = converted_quantity_type

            if ',' in str(spending_amount):
                bla = (str(spending_amount).replace(",", ".").replace(' ',''))
                spending_amount=float(bla.strip(' '))

            print(day, '|', name_of_item, '|', quantity, '|', quantity_type, '|', spending_amount)
            # print(row)
            # print(type(day),'--',day)
            # print(type(quantity), '--', quantity)
            # print(type(quantity_type), '--', quantity_type)
            print('--------')

            test_spend = Spendings(day=day, name_of_item=name_of_item, quantity=quantity, quantity_type=quantity_type,
                                  spending_amount=spending_amount, user_id=1)
            db.session.add(test_spend)
            db.session.commit()

            #dto = datetime.strptime(date_str, '%d.%m.%Y').date()

    else:
        day = datetime.strptime(day_value, '%d.%m.%Y').date()

# output csv to import
