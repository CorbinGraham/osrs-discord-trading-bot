import requests
import time
import copy
import re

# This file fetches all of the pricing data from the OSRS GE HTML pages.
# Priceing data is scraped for the available 180 days of data.
# HTML is used over the API as the API response rate and burst rates are low and unstable.

BASE_URL = 'http://services.runescape.com/m=itemdb_oldschool/'
class price_fetcher:

	# Need to add checks to make sure that each of the pages return data.
	def fetch_id_prices(self, ids_and_items):
		id_with_pricing_info = dict()

		for item_id in ids_and_items:
			successful = False
			while not successful:
				#import pdb; pdb.set_trace()
				url = BASE_URL + ids_and_items[item_id].replace(' ', '+') + '/viewitem?obj=' + str(item_id) 
				print(item_id)
				
				# Try to fetch raw HTML from osrs ge item pages.
				try:
					# If we can't read the text, the response is empty.
					page = requests.get(url)

					# if we hit a 404 error don't keep attempting the item as it likely does not exist.
					if page.status_code == 404:
						break
					page = page.text

				except:
					# Sleep longer because we failed
					print('failed on ' + ids_and_items[item_id])
					time.sleep(5)
					continue
				

				successful = True

				page = self.parse_html(page)
				
				id_with_pricing_info.update([(item_id, page)])
				
				# Not sleeping here since each HTML request takes ~2 seconds anyways.				

		return id_with_pricing_info

	# Accepts the HTML page in its raw form and returns a dict of form [date: price_on_date, date2: price_on_date2]
	def parse_html(self, page):
		# A regex to find all of the price points over the past 180 days
		list_of_180_price_points = re.findall(r'average180.push.*;', page)
		dates_to_price = dict()

		for price_point in list_of_180_price_points:
			date = price_point[27:37].replace('/', '-') # Conforming to date style of YYYY-MM-dd

			price_point_split = price_point.split(',')
			daily_price = price_point_split[1].strip(' ') # Not using daily price right now but will likely add in future
			moving_average_price = int(price_point_split[2][1:-3]) # Strips extra characters

			dates_to_price.update([(date, moving_average_price)])

		return dates_to_price