import csv
import math
from datetime import datetime, timedelta


# Date_today is left as a datetime object so we can do date calculations from it.
date_today = datetime.date(datetime.now())


date_yesterday = str(date_today - timedelta(days=1))
date_two_days_ago = str(date_today - timedelta(days=2))
date_one_week_ago = str(date_today - timedelta(days=8))

TEN_PERCENT_HEADER = [['Ten % Drop in Single Day'],
					  ['Item Name', 'Price Yesterday', 'Price Today', 'Percent Change']]
TWENTY_PERCENT_HEADER = [['Twenty % Drop in One Week'],
						 ['Item Name', 'Price Last Week', 'Todays Price', 'Percent Change']]
LOWEST_PRICE_HEADER = [['Lowest Price in 180 Days'],
					   ['Item Name', 'Highest Price in 180 Days', 'Date of Highest Price', 'Percent Change from 180 Day High', 'Previous lowest price', 'Previous Lowest Price Date' 'Todays Price', 'Percent Below Previous Min']]

class analyzer:

	def analyze(self, ids_to_dates_and_prices, ids_to_item_name):
		# The date will be the name of the outputted CSV

		# These will be filled with the appropriate datasets before being placed into the CSV.
		prepped_ten_percent_csv_row = []
		prepped_twenty_percent_csv_row = []
		prepped_180_day_low_csv_row = []

		for item_id in ids_to_dates_and_prices:
			self.ten_percent_drop_in_one_day(ids_to_dates_and_prices[item_id], item_id, prepped_ten_percent_csv_row, ids_to_item_name)
			self.twenty_percent_drop_in_one_week(ids_to_dates_and_prices[item_id], item_id, prepped_twenty_percent_csv_row, ids_to_item_name)
			self.lowest_price_in_180_days(ids_to_dates_and_prices[item_id], item_id, prepped_180_day_low_csv_row, ids_to_item_name)

		self.push_data_to_csv(prepped_ten_percent_csv_row, prepped_twenty_percent_csv_row, prepped_180_day_low_csv_row)


	def ten_percent_drop_in_one_day(self, item_prices, item_id, row_list, ids_to_item_name):
		percent_change = abs(item_prices[date_two_days_ago] - item_prices[date_yesterday]) / ((item_prices[date_two_days_ago] + item_prices[date_yesterday]) / 2)

		# Preps the CSV row if true.
		if percent_change >= 0.1:
			row_list.append([ ids_to_item_name[item_id],
							 item_prices[date_two_days_ago],
							 item_prices[date_yesterday],
							 percent_change * 100
							])

	def twenty_percent_drop_in_one_week(self, item_prices, item_id, row_list, ids_to_item_name):
		percent_change = abs(item_prices[date_one_week_ago] - item_prices[date_yesterday]) / ((item_prices[date_one_week_ago] + item_prices[date_yesterday]) / 2)

		print(percent_change)

		if percent_change >= 0.2:
			row_list.append([ ids_to_item_name[item_id],
							 item_prices[date_one_week_ago],
							 item_prices[date_yesterday],
							 percent_change * 100
							])
	# All API calls give us 180 days of data. This checks to see if today is the lowest price in 180 days.
	def lowest_price_in_180_days(self, item_prices, item_id, row_list, ids_to_item_name):
		current_price = item_prices[date_yesterday]
		lowest_price = math.inf
		lowest_price_date = ''

		highest_price = 0
		highest_price_date = ''


		for price_date in item_prices:
			# If any price is below todays, return instantly.
			if item_prices[price_date] < current_price:
				return

			# Update the previous lowest price
			if item_prices[price_date] < lowest_price and str(date_yesterday) != price_date:
				lowest_price = item_prices[price_date]
				lowest_price_date = price_date

			# Find the highest price in the last 180 days
			if item_prices[price_date] > highest_price and str(date_yesterday) != price_date:
				highest_price = item_prices[price_date]
				highest_price_date = price_date

		percent_change_to_lowest = abs(item_prices[lowest_price_date] - item_prices[date_yesterday]) / ((item_prices[lowest_price_date] + item_prices[date_yesterday]) / 2)
		percent_change_to_highest = abs(item_prices[highest_price_date] - item_prices[date_yesterday]) / ((item_prices[highest_price_date] + item_prices[date_yesterday]) / 2)

		row_list.append([ids_to_item_name[item_id],
						 highest_price,
						 highest_price_date,
						 percent_change_to_highest * 100,
						 lowest_price,
						 lowest_price_date,
						 current_price,
						 percent_change_to_lowest * 100
						 ])

	def push_data_to_csv(self, one_day_drop, weekly_drop, overall_low):
		with open('../output/' + str(date_today) + '.csv', 'w', newline='') as file:
			writer = csv.writer(file)
			writer.writerows(TEN_PERCENT_HEADER)
			writer.writerows(one_day_drop)

			writer.writerows(TWENTY_PERCENT_HEADER)
			writer.writerows(weekly_drop)

			writer.writerows(LOWEST_PRICE_HEADER)
			writer.writerows(overall_low)