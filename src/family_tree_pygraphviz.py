import pygraphviz as pgv
from member import MemberNode


def get_node_color(memberNode_obj):
    node_color = 'pink' if memberNode_obj.sex == 0 else 'black'
    return node_color


def get_struct_info(memberNode_obj):
    print("line：11",memberNode_obj.member_name, memberNode_obj.member_id, memberNode_obj.descent_no, memberNode_obj.spouse_name)
    spouse_name  = memberNode_obj.spouse_name if memberNode_obj.spouse_name is not None else ''
    # label内容若由大括号包含，则按行展示，否则，则按列展示
    # spouse_name 若为汉字，则显示为空，原因在于：port 之后必须有空格，否则无法显示汉字。
    struct_info = "{{<member_name> " + memberNode_obj.member_name + "}" + "|{<descent_no> " + str(memberNode_obj.descent_no) + "}" + "|{<spouse_name> " + spouse_name + "}}"
    return struct_info


# 处理当前成员节点
def draw_node(G, member_dict, cur_node):
    print(cur_node.member_name)
    cur_member_id = cur_node.member_id
    member_obj = member_dict.get(cur_node.member_id)

    cur_struct_info = get_struct_info(cur_node)
    G.add_node(cur_member_id, label=cur_struct_info, color=get_node_color(cur_node))

    if member_obj is None:
        print("member_id:{member_id} not exist".format(member_id=cur_member_id))

    member_obj.legal_child_list.sort(key=lambda child_obj: child_obj.order_seq)
    for son_member_obj in member_obj.legal_child_list[::-1]:
        son_spouse_name = son_member_obj.spouse_name if son_member_obj.spouse_name is not None else ""
        classname = "middle-level" if son_member_obj.sex is 1 else "product-dept"
        child_node = MemberNode(son_member_obj.member_id, son_member_obj.member_name, son_member_obj.sex,
                                son_member_obj.descent_no, son_spouse_name, classname)

        child_struct_info = get_struct_info(child_node)
        G.add_node(child_node.member_id, label=child_struct_info, color=get_node_color(child_node))

        G.add_edge(cur_member_id, child_node.member_id, headport='', tailport='')
        draw_node(G, member_dict, child_node)


def draw_tree(member_dict, first_member_id, filename, title_name):
    G = pgv.AGraph(strict=False, overlap=False)
    G.graph_attr['label'] = title_name
    G.graph_attr['labelloc'] = 't' # 图名字位置在上面 t, 在下面 b
    G.graph_attr['labeljust'] = 'r' # 图名字位置在左侧 l, 在右侧 r
    G.graph_attr['rankdir'] = 'TB'
    G.graph_attr['splines'] = 'ortho'
    G.node_attr['shape'] = 'record'
    G.layout(prog='dot')


    # 获取到第一个成员节点
    member_obj = member_dict.get(first_member_id)
    member_name = member_obj.member_name
    sex = member_obj.sex
    spouse_name = member_obj.spouse_name
    descent_no = member_obj.descent_no

    first_member_node = MemberNode(first_member_id, member_name, sex, descent_no, spouse_name, "middle-level")
    draw_node(G, member_dict, first_member_node)

    G.draw(filename, format='svg', prog='dot')

