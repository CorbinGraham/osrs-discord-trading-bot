path = '../tradable_items.txt'

# Reads in text file containing ids and tradeable items
def read_item_ids():
	item_id_dic = dict()
	with open(path, 'r') as file:
	    for line in file:
	    	line = line.strip()
	    	if line == '':
	    			continue
	    	split_line = line.split(':')
	    	item_id_dic.update([(int(split_line[0]), split_line[1][1:])])

	return item_id_dic

