# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import json


def append_line_to_file(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line + '\n')


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


# Example usage


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dict = read_json_file('data.json')
    for item in dict['data']['models']:
        append_line_to_file('test.md', '### ' + item['owner'] + '/' + '*' + item['name'] + '*')
        append_line_to_file('test.md', '#### ' + item['description'])
        # append_line_to_file('test.md', "#### ![Alt text]({})".format(item['cover_image_url']))
        append_line_to_file('test.md', "\n<img src=\"{}\" alt=\"image\" width=\"300\" height=\"auto\">\n".format(
            item['cover_image_url']))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
