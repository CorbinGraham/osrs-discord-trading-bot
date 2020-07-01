path = '../bin/tradable_items.txt'

# Input: File containing items names and ids of form (id: name)
# Output: dict() of form {id: name, id2: name2}
# Reads in text file containing ids and tradeable items
def read_item_ids():
	item_id_dic = dict()
	with open(path, 'r') as file:
	    for line in file:
	    	line = line.strip()
	    	if line == '': # skip any empty rows
	    			continue
	    	split_line = line.split(':')
	    	item_id_dic.update([(int(split_line[0]), split_line[1][1:])])

	return item_id_dic

