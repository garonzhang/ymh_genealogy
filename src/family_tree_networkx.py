import json
from member import MemberNode
import networkx as nx
import matplotlib.pyplot as plt


def draw_node(member_dict, cur_node, data_part):
    print(cur_node.member_name)
    cur_member_id = cur_node.member_id
    member_obj = member_dict.get(cur_node.member_id)
    if member_obj is None:
        print("member_id:{member_id} not exist".format(member_id=cur_member_id))

    member_obj.legal_child_list.sort(key=lambda child_obj: child_obj.order_seq)
    for son_member_obj in member_obj.legal_child_list[::-1]:
        son_spouse_name = son_member_obj.spouse_name if son_member_obj.spouse_name is not None else ""
        classname = "middle-level" if son_member_obj.sex is 1 else "product-dept"
        child_node = MemberNode(son_member_obj.member_id, son_member_obj.member_name, son_member_obj.sex,son_spouse_name,
                                son_member_obj.descent_no, classname)
        cur_node.add_child(child_node)
        data_part.append((cur_member_id, son_member_obj.member_id))
        draw_node(member_dict, child_node, data_part)


def get_data_part(member_dict, first_member_id):
    data_part = []

    # 获取成员基本信息
    member_obj = member_dict.get(first_member_id)
    member_name = member_obj.member_name
    sex = member_obj.sex
    spouse_name = member_obj.spouse_name
    descent_no = member_obj.descent_no

    first_node = MemberNode(first_member_id, member_name, sex, spouse_name, descent_no, "middle-level")
    draw_node(member_dict, first_node, data_part)

    return data_part


def draw_tree(member_dict, first_member_id, file_name):
    data_part = get_data_part(member_dict, first_member_id)
    G = nx.DiGraph()
    G.add_edges_from(data_part)
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=False, arrows=False, node_shape='s', node_size=2, alpha=0.5, font_size=1)
    plt.savefig('../output/nx_familytree.svg')
