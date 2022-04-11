from calendar import monthrange


def plan_to_dict(month_plan):
	planDict = {}
	days = monthrange(month_plan.month.year, month_plan.month.month)[1]

	for month_type in month_plan.list_of_planned_spending:
		planDict[f'{month_type.name_of_type}'] = {
			'id':month_type.id,
			'name': f'{month_type.name_of_type}',
			'amount_in_money': round(month_type.amount_in_money, 2),
			'amount_in_percent': round(month_type.amount_in_percent, 2),
			'daily': round(month_type.amount_in_money / days, 2) if month_type.is_everyday else False,
		}
	return planDict


def daily_overall_dict(month_dict, income_value):
	overall_day_amount = 0
	overall_day_percent = 0
	overall_day_daily = 0
	overall_month_amount = 0
	overall_month_percent = 0

	left_percent = 100
	overall_amount_types = 0

	for i in month_dict:
		if month_dict[i]['daily']:
			overall_day_amount += month_dict[i]['amount_in_money']
			overall_day_percent += month_dict[i]['amount_in_percent']
			overall_day_daily += month_dict[i]['daily']
		elif not month_dict[i]['daily']:
			overall_month_amount += month_dict[i]['amount_in_money']
			overall_month_percent += month_dict[i]['amount_in_percent']
		left_percent -= month_dict[i]['amount_in_percent']
		overall_amount_types += month_dict[i]['amount_in_money']
	overall_percent = 100 - left_percent

	if left_percent < 100:
		left_amount = income_value - overall_amount_types
	else:
		left_amount = overall_amount_types

	return {
		'overall_day_percent': round(overall_day_percent, 2),
		'overall_day_amount': round(overall_day_amount, 2),
		'overall_day_daily': round(overall_day_daily, 2),

		'overall_month_percent': round(overall_month_percent, 2),
		'overall_month_amount': round(overall_month_amount, 2),

		'left_percent': round(left_percent, 2),
		'left_amount': round(left_amount, 2),
	}
