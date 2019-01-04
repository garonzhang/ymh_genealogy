import pygraphviz as pgv
from queue import Queue


def get_root_style():
    root_style = {'color': 'green',
                  'style': 'filled',
                  'fillcolor': '#FF4500',
                  'shape': 'circle',
                  'label': '',
                  'width': 0.5,
                  'fixedsize': 'true'}
    return root_style


def get_child_style(child_obj):
    node_color1 = 'OrangeRed' if child_obj.sex == 0 else 'DarkTurquoise'
    node_color2 = 'OrangeRed' if child_obj.sex == 0 else 'SpringGreen'
    node_color3 = 'OrangeRed' if child_obj.sex == 0 else 'DeepSkyBlue'
    node_color4 = 'OrangeRed' if child_obj.sex == 0 else '#00FFFF'
    node_color5 = 'OrangeRed' if child_obj.sex == 0 else '#98FB98'
    ###node_color = 'OrangeRed' if child_obj.descent_no % 2 == 0 else '#98FB98'
    node_color = 'SpringGreen'
    width = 0.07

    # 针对 dudu，单独处理
    if child_obj.member_id == 1809:
        node_color = '#FFEC8B'
        width = 0.1
    child_style = {'color': node_color, 'shape': 'point', 'label': '', 'width': width}
    return child_style


def get_edge_style(child_obj):
    edge_color1 = 'DeepSkyBlue' if child_obj.sex == 0 else 'SpringGreen'
    ###edge_color = '#40E0D0' if child_obj.descent_no % 2 == 0 else 'SpringGreen'
    edge_color = 'DeepSkyBlue'#'#20B2AA'
    style = 'dashed'#''dotted' 'dashed' 'solid'
    edge_style = {'color': edge_color, 'weight': 0.0, 'style': style}
    return edge_style


# 构造世系环状图
def construct_graph(g, member_dict, first_member_id):
    member_queue = Queue()

    member_obj = member_dict.get(first_member_id)
    if member_obj is None:
        print("construct_graph(): member_id:{member_id} not exist".format(member_id=first_member_id))
        return

    g.add_node(member_obj.member_id, **get_root_style())
    member_queue.put(member_obj)

    while not member_queue.empty():
        member_obj = member_queue.get()

        child_list = sorted(member_obj.child_list, key=lambda child: child.order_seq)
        for child_obj in child_list:
            if child_obj.step_father_id is None or child_obj.step_father_id == member_obj.member_id:
                member_queue.put(child_obj)
                g.add_node(child_obj.member_id, **get_child_style(child_obj))
                g.add_edge(member_obj.member_id, child_obj.member_id, **get_edge_style(child_obj))


def gen_graph(member_dict, first_member_id):
    img_formats = ['svg']#'png', 'svg']
    for img_format in img_formats:
        filename = '../output/whole_family.' + img_format
        g = pgv.AGraph(bgcolor='#000000', format=img_format, ranksep=0.4, nodesep=30, root=1)
        construct_graph(g, member_dict, first_member_id)
        g.layout(prog='twopi')
        g.draw(filename)
