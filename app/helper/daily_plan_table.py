import pandas as pd


def delta_flow_test(start, end, daily_query, month_day_income):
	planDict = {}

	dates_list = pd.date_range(start, end, freq='D')

	income = month_day_income

	day_start = income
	day_result = 0

	average_for_day = income / len(dates_list)

	static_delta_overall = 0

	for date in dates_list:
		day_start += day_result
		day_result = -sum(float(c.spending_amount) for c in daily_query.filter_by(day=date).all())

		delta = (end - date.date()).days
		dynamic_mid = day_start / (delta + 1)

		if delta != 0:
			dynamic_delta = (day_start + day_result) / delta - dynamic_mid
		else:
			dynamic_delta = (day_start + day_result)

		static_mid = average_for_day + static_delta_overall
		static_delta_day = static_mid + day_result - static_delta_overall
		static_delta_overall = static_mid + day_result

		planDict[f'{date.date().strftime("%d.%m")}'] = {
			'day_start': round(day_start, 2),
			'day_result': round(day_result, 2),
			'dynamic_delta': round(dynamic_delta, 2),
			'dynamic_mid': round(dynamic_mid, 2),
			'static_mid': round(static_mid, 2),
			'static_delta_day': round(static_delta_day, 2),
			'static_delta_overall': round(static_delta_overall, 2),
		}

	return planDict
