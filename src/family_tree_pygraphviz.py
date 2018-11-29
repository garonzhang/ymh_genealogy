import pygraphviz as pgv


def get_point_count(sons_list):
    sons_count = len(sons_list)
    point_count = sons_count if sons_count % 2 != 0 else sons_count + 1
    return point_count


def draw_tree(member_dict):
    G = pgv.AGraph(strict=False, overlap='false')
    G.graph_attr['rankdir'] = 'TB'
    G.graph_attr['splines'] = 'ortho'
    G.node_attr['shape'] = 'record'

    G.layout(prog='dot')

    # 创建各节点及各节点的垂直向下 point，用作与其子节点的连接点
    for member_id, member_obj in member_dict.items():
        #print(member_id, member_obj.member_name)

        spouse_name = member_obj.spouse_name
        if spouse_name is None:
            spouse_name = ""

        # label内容若由大括号包含，则按行展示，否则，则按列展示
        # spouse_name 若为汉字，则显示为空，原因在于：port 之后必须有空格，否则无法显示汉字。
        struct_info = "{{<member_name> " + member_obj.member_name + "|<descent_no> " + str(member_obj.descent_no) +"}"+\
                      "|<spouse_name> " + spouse_name + "}"
        G.add_node(member_id,label=struct_info)

        # 生成当前 member 节点下方的 point 集合
        point_list = []
        point_count = get_point_count(member_obj.sons_list)
        for order in range(point_count):
            point_id = "p"+str(order) + str(member_id)
            G.add_node(point_id, shape='point')
            #G.add_node(point_id, shape='point', style='invisible')
            point_list.append(point_id)

        # 确保生成的 N 个 point 处于同一水平位置
        G.add_subgraph(point_list, rank='same')

        # 连接当前 member 节点与生成的 N 个 point 中处于中间位置的 point
        print("member_id = ", member_id, member_obj.member_name)
        G.add_edge(member_id, "p"+str(int(point_count/2)) + str(member_id), arrowhead='none')

        # 将生成的 N 个 point 点顺次连接
        for i in range(point_count - 1):
            G.add_edge(point_list[i],point_list[i + 1], arrowhead='none',color='black',shape='ortho')

    # 将各节点下方的各 point 与其儿子 member 节点连接起来
    for member_id, member_obj in member_dict.items():
        sons_list = member_obj.sons_list
        for order in range(len(sons_list)):
            point_index = order
            if len(sons_list) %2 == 0 and point_index >= int(len(sons_list)/2):
                point_index = point_index + 1
            point_id = "p" + str(point_index) + str(member_id)
            G.add_edge(point_id, sons_list[order], arrowhead='none',color='black')
        for index in range(len(sons_list)-1):
            G.add_edge(sons_list[index], sons_list[index + 1], arrowhead='none',color='black')
        G.add_subgraph(sons_list, rank='same')

    G.draw("../data/familytree.svg", format='svg', prog='dot')

