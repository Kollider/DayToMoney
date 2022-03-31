from calendar import monthrange


def plan_to_dict(month_plan):
	planDict = {}
	days = monthrange(month_plan.month.year, month_plan.month.month)[1]

	for month_type in month_plan.list_of_planned_spending:
		planDict[f'{month_type.name_of_type}'] = {
			'name': f'{month_type.name_of_type}',
			'amount_in_money': month_type.amount_in_money,
			'amount_in_percent': month_type.amount_in_percent,
			'daily': round(month_type.amount_in_money / days, 2) if month_type.is_everyday else False,
		}
	return planDict


def daily_overall_dict(month_dict):
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
	if left_percent<100:
		left_amount = round(overall_amount_types /((100 - left_percent)/100),2) - overall_amount_types # #todo check if left_amount is correct
	else:
		left_amount = overall_amount_types
	print(overall_amount_types,overall_percent,left_amount, left_percent)

	return {
		'overall_day_percent': overall_day_percent,
		'overall_day_amount': overall_day_amount,
		'overall_day_daily': overall_day_daily,

		'overall_month_percent': overall_month_percent,
		'overall_month_amount': overall_month_amount,

		'left_percent': left_percent,
		'left_amount': left_amount
	}
