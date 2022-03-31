def list_categories(file):
    with open(file) as minifigures:
        categories_list = []
        for line in minifigures:
            if 'Category ID' in line:
                continue
            content = line.strip().split('\t')
            if len(content) < 2:
                continue
            category_id = content[0]
            if category_id not in categories_list:
                categories_list.append(category_id)
    return categories_list

categories = list_categories('minifigures.txt')

with open('categories.json', 'w') as json_file:
    for element in categories:
        minifigures_list = []
        with open('minifigures.txt') as textfile:
            for line in textfile:
                if 'Category ID' in line:
                    continue
                content = line.strip().split('\t')
                if len(content) < 2:
                    continue
                if content[0] != element:
                    continue
                minifigures_list.append(content[2])
        json_file.write('{\'category_id\': ' + str(element) + ',\'minifigure_ids\': ' + str(minifigures_list) + '}')




