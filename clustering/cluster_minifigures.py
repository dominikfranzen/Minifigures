import json

def parse_content_line(line):
    if 'Category ID' in line:
        return False
    content = line.strip().split('\t')
    if len(content) < 2:
        return False
    else:
        return content

def list_categories(file):
    with open(file) as minifigures:
        categories_list = []
        for line in minifigures:
            if parse_content_line(line) == False:
                continue
            category_id = parse_content_line(line)[0]
            if category_id not in categories_list:
                categories_list.append(category_id)
    return categories_list

def sort_minifigures_to_categories(list):
    dict_list = []
    for element in list:
        minifigures_list = []
        with open('minifigures.txt') as textfile:
            for line in textfile: 
                if parse_content_line(line) == False:
                    continue
                if parse_content_line(line)[0] != element:
                    continue
                minifigures_list.append(parse_content_line(line)[2])
        dict_to_add = {
            'category_id': element,
            'minifigure_ids': minifigures_list
        }
        dict_list.append(dict_to_add)
    return dict_list

def write_json_file(data):
    with open('categories.json', 'w') as json_file:
        json_file.write(json.dumps(data))

categories = list_categories('minifigures.txt')
content_for_json_file = sort_minifigures_to_categories(categories)
write_json_file(content_for_json_file)



