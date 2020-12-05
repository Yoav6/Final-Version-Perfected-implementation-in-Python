#  inspired by
#  https://www.lesswrong.com/posts/xfcKYznQ6B9yuxB28/final-version-perfected-an-underused-execution-algorithm

import json

to_do_list = []

def startup():
    while True:
        user_input = input("""What would you like to do?
1: add item
2. prioritize items
""")
        if user_input == '1':
            add_item()
        elif user_input == '2':
            if to_do_list:
                marked_item_index, next_index, marked_item = prepare_list()
                prioritize(marked_item_index, next_index, marked_item)
            else:
                print('your to-do list is empty! you must first add items to it! \n')
        else:
            print(f'"{user_input}" is invalid, please try again')

def add_item():
    while True:
        item = [input('enter a task (or blank to go back): '), 'unmarked']
        if item[0]:
            to_do_list.append(item)
            update_json()
        else:
            print('')
            break

def prepare_list():
    to_do_list[0][1] = 'marked'
    marked_item_index, next_index, marked_item = 0, 1, to_do_list[0]
    for index, item in enumerate(to_do_list):
        if item[1] == 'marked':
            marked_item_index, next_index, marked_item = index, index + 1, item
    return marked_item_index, next_index, marked_item

def prioritize(marked_item_index, next_index, marked_item):
    while True:
        print('')
        try:
            next_item = to_do_list[next_index][0]
        except IndexError:
            print("=== '" + marked_item[0] + "'", 'has been chosen and crossed off the list ===\n')
            to_do_list.pop(marked_item_index)
            update_json()
            break
        else:
            user_input = input(f"""Which do you want to do more?
1: {marked_item[0]}
2: {next_item}
""")
            if user_input == '2':
                to_do_list[next_index][1] = 'marked'
                marked_item = to_do_list[next_index]
                marked_item_index = next_index
            next_index += 1
            update_json()

def update_json():
    with open('list.json', 'w') as f:
        json.dump(to_do_list, f, indent=2)


try:
    with open('list.json', 'r') as f:
        to_do_list = json.load(f)
except FileNotFoundError:
    pass
except json.decoder.JSONDecodeError:
    pass

startup()
