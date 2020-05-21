import os


def remove_blank_spaces(string_list):
    washed_list = []
    for elem in string_list:
        if elem != '':
            washed_list.append(elem)
    return washed_list


def is_string_left_curly_bracket(string):
    split_string = string.split(' ')
    washed_string = remove_blank_spaces(split_string)
    return washed_string[0] == "{"


class Armor_category:
    def __init__(self, category):
        self.category = category
        self.items = []

    def add_item(self, item):
        self.items.append(item)


file = "/../wow_library/include/Armory.hpp"
path = os.getcwd() + file
file1 = open(path, "r")
lines = file1.readlines()
file1.close()

armor_types = []
found_item_vector = False
for line in lines:
    line1 = line.split(' ')
    line1 = remove_blank_spaces(line1)
    if line1[0] == 'std::vector<Armor>':
        if line1[1][-3:-1] == '_t':
            armor = Armor_category(line1[1][0:-3])
            found_item_vector = True

    if found_item_vector:
        line2 = line.split('"')
        if len(line2) == 3:
            if is_string_left_curly_bracket(line2[0]):
                armor.add_item(line2[1])

    if line1[0] == '};\n' and found_item_vector:
        found_item_vector = False
        armor_types.append(armor)

weapons = []
found_item_vector = False
for line in lines:
    line1 = line.split(' ')
    line1 = remove_blank_spaces(line1)
    if line1[0] == 'std::vector<Weapon>':
        if line1[1][-3:-1] == '_t':
            armor = Armor_category(line1[1][0:-3])
            found_item_vector = True

    if found_item_vector:
        line2 = line.split('"')
        if len(line2) == 3:
            if is_string_left_curly_bracket(line2[0]):
                armor.add_item(line2[1])

    if line1[0] == '};\n' and found_item_vector:
        found_item_vector = False
        weapons.append(armor)

all_weapons = []
for wep_type in weapons:
    for item in wep_type.items:
        all_weapons.append(item)

# write to yaml
# file1 = open("items.yml", "w")
# for armor_type in armor_types:
#     file1.write(armor_type.category + ":\n")
#     for item in armor_type.items:
#         file1.write("    - " + item + "\n")
# file1.close()

with open("index.html", "r") as f:
    lines = f.readlines()

washed_lines = []
copy_line = True
armor_index = 0
found_start = False
found_stop = False
for index, line in enumerate(lines):
    l = line
    if copy_line:
        washed_lines.append(line)
    if line == "<!--armor begin-->\n":
        found_start = True
        armor_index = index
        copy_line = False
    if line == "<!--armor stop-->\n":
        found_stop = True
        washed_lines.append(line)
        copy_line = True

dropdowns_in_a_row = 0
if found_start and found_stop:
    first_part = washed_lines[0:armor_index + 1]
    second_part = washed_lines[armor_index + 1:-1]

    # Armor selection
    generated_1 = []
    for armor_type in armor_types:
        if armor_type.category == 'ring' or armor_type.category == 'trinket':
            for i in range(2):
                generated_1.append('<select id="' + armor_type.category + '_dd' + str(i+1) + '" onchange="read_drop_down()">\n')
                generated_1.append(
                    '    <option value="none" selected disabled>' + armor_type.category + str(i + 1) + '</option>\n')
                for item in armor_type.items:
                    generated_1.append('    <option value="' + item + '">' + item + '</option>\n')
                generated_1.append('</select>\n')
                generated_1.append('\n')
                dropdowns_in_a_row = dropdowns_in_a_row + 1
        else:
            generated_1.append('<select id="' + armor_type.category + '_dd" onchange="read_drop_down()">\n')
            generated_1.append('    <option value="none" selected disabled>' + armor_type.category + '</option>\n')
            for item in armor_type.items:
                generated_1.append('    <option value="' + item + '">' + item + '</option>\n')
            generated_1.append('</select>\n')
            generated_1.append('\n')
            dropdowns_in_a_row = dropdowns_in_a_row + 1

        if dropdowns_in_a_row >= 4:
            generated_1.append('<p></p>\n')
            generated_1.append('\n')
            dropdowns_in_a_row = 0

    # Weapon selection
    alternatives = ["main_hand", "off_hand"]
    generated_2 = ['<p> Select weapons: </p>\n']
    for i in range(2):
        generated_2.append('<select id="' + alternatives[i] + '_dd" onchange="read_drop_down()">\n')
        generated_2.append('    <option value="none" selected disabled>' + alternatives[i] + '</option>\n')
        for item in all_weapons:
            generated_2.append('    <option value="' + item + '">' + item + '</option>\n')
        generated_2.append('</select>\n')
        generated_2.append('\n')

    file1 = open("generated.html", "w")
    for line in first_part:
        file1.write(line)
    for line in generated_1:
        file1.write(line)
    for line in generated_2:
        file1.write(line)
    for line in second_part:
        file1.write(line)
    file1.close()
else:
    print("WARNING: no start of stop found")