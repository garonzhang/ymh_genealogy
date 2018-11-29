import json
from member import MemberNode
import networkx as nx
import matplotlib.pyplot as plt


def hierarchy_pos(G, root, width=2000., vert_gap=500, vert_loc=0, xcenter = 0.5,
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    if parent != None:   #this should be removed for directed graphs.
        neighbors.remove(parent)  #if directed, then parent not in neighbors.
    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G, neighbor, width=dx*100, vert_gap=vert_gap*200,
                                vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                parent=root)
    return pos


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

    # [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10),
    #                       (5, 11), (5, 12), (6, 13), (7, 14), (7, 15), (7, 16), (8, 17), (8, 18), (8, 19)]


def draw_tree(member_dict, first_member_id, file_name):
    data_part = get_data_part(member_dict, first_member_id)
    G = nx.Graph()
    G.add_edges_from(data_part)
    pos = hierarchy_pos(G, first_member_id)
    nx.draw(G, pos=pos, with_labels=True)
    plt.savefig(file_name)

