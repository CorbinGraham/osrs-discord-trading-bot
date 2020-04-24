from read_item_ids import read_item_ids
from price_fetcher import price_fetcher

def main():
	item_ids_and_names = read_item_ids()

	price_fetch = price_fetcher()

	item_ids_with_pricing = price_fetch.fetch_id_prices(item_ids_and_names)

	

main()
