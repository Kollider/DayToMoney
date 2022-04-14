from app.helper.converter import converter


def validate_spendings(spending):
	spending.quantity, spending.quantity_type = converter((spending.quantity, spending.quantity_type))
	return spending
