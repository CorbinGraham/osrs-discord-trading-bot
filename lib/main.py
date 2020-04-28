from read_item_ids import read_item_ids
from price_fetcher import price_fetcher
from analyzer import analyzer

def main():
	# Read in all of the ids and item names.
	item_ids_and_names = read_item_ids()

	# Fetch all of the pricing for all the ids from the OSRS GE API
	price_fetch = price_fetcher()
	item_ids_with_pricing = price_fetch.fetch_id_prices(item_ids_and_names)

	# Compile the fetched pricing data into a usable CSV.
	analyzer_object = analyzer()
	analyzer_object.analyze(item_ids_with_pricing, item_ids_and_names)


	

main()
