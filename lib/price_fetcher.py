import requests
import time
import copy

# This file fetches all of the pricing data from the OSRS GE API.
#https://www.reddit.com/r/2007scape/comments/3g06rq/guide_using_the_old_school_ge_page_api/

BASE_URL = 'http://services.runescape.com/m=itemdb_oldschool'
class price_fetcher:

	# Need to add checks to make sure that each of the pages return data.
	def fetch_id_prices(self, ids_and_items):
		id_with_pricing_info = dict()
		for item_id in ids_and_items:
			url = BASE_URL + '/api/graph/' + str(item_id) + '.json'  
			page = requests.get(url).json()

			page = self.convert_to_dates(page)
			import pdb; pdb.set_trace()
			
			id_with_pricing_info.update([(item_id, page)])
			print(page)

			# Sleep, so we don't get timed out
			time.sleep(0.5)

		return id_with_pricing_info

	# Times are all presented in Epoch from the API
	# This method converts them to YYYY-MM-dd
	def convert_to_dates(self, item_json):
		# We need to copy the JSON since we can't replace keys
		item_json_copy = copy.deepcopy(item_json)
		for epoch_time in item_json['daily']:
			converted_date = time.strftime('%Y-%m-%d', time.localtime(int(epoch_time[0:-3])))
			item_json_copy['daily'][converted_date] = item_json['daily'][epoch_time]
			item_json_copy['daily'].pop(epoch_time, None)

		for epoch_time in item_json['average']:
			converted_date = time.strftime('%Y-%m-%d', time.localtime(int(epoch_time[0:-3])))
			item_json_copy['average'][converted_date] = item_json['average'][epoch_time]
			item_json_copy['average'].pop(epoch_time, None)
		
		return item_json_copy


