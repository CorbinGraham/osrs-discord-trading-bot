import requests
import time
import copy

# This file fetches all of the pricing data from the OSRS GE API.
#https://www.reddit.com/r/2007scape/comments/3g06rq/guide_using_the_old_school_ge_page_api/

# Need to modify this to scrape directly from the osrs 
# http://services.runescape.com/m=itemdb_oldschool/Zulrah%27s+scales/viewitem?obj=12934
BASE_URL = 'http://services.runescape.com/m=itemdb_oldschool'
class price_fetcher:

	# Need to add checks to make sure that each of the pages return data.
	def fetch_id_prices(self, ids_and_items):
		id_with_pricing_info = dict()

		for item_id in ids_and_items:
			successful = False
			while not successful:
				import pdb; pdb.set_trace()
				url = BASE_URL + '/api/graph/' + str(item_id) + '.json'  
				print(item_id)
				
				# Try to fetch price data from API
				try:
					# If we can't convert to a JSON, the response is empty.
					page = requests.get(url)

					# if we hit a 404 error don't keep attempting the item.
					if page.status_code == 404:
						break
					page = page.json()

				except:
					# Sleep longer because we failed
					print('failed on' + ids_and_items[item_id])
					time.sleep(20)
					continue
				

				successful = True
				page = self.convert_to_dates(page)
				
				id_with_pricing_info.update([(item_id, page)])

				# Sleep, so we don't get timed out
				time.sleep(0.5)				

		return id_with_pricing_info

	# Times are all presented in Epoch from the API
	# This method converts them to YYYY-MM-dd
	def convert_to_dates(self, item_json):
		# We aren't using the 'daily' data so we are just going to pop them from the JSON
		item_json.pop('daily', None)

		# Update the keys from an Epoch time to form 'YYYY-mm-dd'
		for epoch_time in item_json['average']:
			converted_date = time.strftime('%Y-%m-%d', time.localtime(int(epoch_time[0:-3])))
			item_json[converted_date] = item_json['average'][epoch_time]

		# Simplifies the JSON since we've updated the keys
		item_json.pop('average', None)
			
		return item_json


