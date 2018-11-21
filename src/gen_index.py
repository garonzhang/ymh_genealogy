
from xpinyin import Pinyin

p = Pinyin()


class Node:
    def __init__(self,member_name, pinyin, page_no):
        self.member_name  = member_name
        self.pinyin = pinyin
        self.page_no = page_no


def get_pinyin(chinese_word):
    if chinese_word == "聁":
        result = "pan"
    elif chinese_word == "聨":
        result = "lian"
    elif chinese_word == "凖":
        result = "zhun"
    else:
        result = p.get_pinyin(chinese_word, '')
    return result


def add_node(node):
    pinyin = node.pinyin
    capital = pinyin[0:1]

    node_list = page_dict.get(capital, None)
    if node_list is None:
        node_list = []
        node_list.append(node)
        page_dict[capital] = node_list
    else:
        node_list.append(node)


def generate_index(file_name):
    print(file_name)
    with open(file_name, encoding='utf-8') as fh:
        line = fh.readline()
        while line:
            line = line.strip()
            term_list = line.split("	")
            member_name = term_list[0]
            page_no = term_list[1]

            pinyin = ""
            for chinese_word in member_name:
                pinyin = pinyin + get_pinyin(chinese_word) + " "

            item = Node(member_name, pinyin, page_no)
            add_node(item)

            line = fh.readline()


if __name__ == '__main__':
    filename = '../data/page_index.dat'
    page_dict = {}
    generate_index(filename)

    new_dict = [(k, page_dict[k]) for k in sorted(page_dict.keys())]
    for (capital, node_list) in new_dict:
        print("\n",capital.upper())
        node_list = sorted(node_list, key = lambda node_item: [node_item.pinyin])

        for item in node_list:
            print(item.member_name + " " + item.page_no)


