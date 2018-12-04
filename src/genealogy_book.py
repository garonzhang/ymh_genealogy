from queue import Queue


# 用于计算子女数量的汉字表达方式
def get_chinese_number(number):
    if number == 1:
        return "一"
    elif number == 2:
        return "两"
    elif number == 3:
        return "三"
    elif number == 4:
        return "四"
    elif number == 5:
        return "五"
    elif number == 6:
        return "六"
    elif number == 7:
        return "七"
    elif number == 8:
        return "八"
    elif number == 9:
        return "九"
    elif number == 10:
        return "十"
    elif number == 11:
        return "十一"
    elif number == 12:
        return "十二"
    elif number == 13:
        return "十三"
    elif number == 14:
        return "十四"


# 获取父母名字信息
# flag = 1 法律父母， flag = 2 生父母
def get_parent_name(member_dict, member_obj, flag=1):
    parent_name = ""

    father_id = member_obj.father_id if flag == 1 else member_obj.step_father_id
    father_obj = member_dict.get(father_id)

    if father_obj is None:
        print("line_no=45, member_id:{member_id} 's father not exist".format(member_id=member_obj.member_id))
        return ""

    # 兼顾入赘的情况
    if father_obj.sex == 1:
        father_name = father_obj.member_name
        mother_name = father_obj.spouse_name
    else:
        father_name = father_obj.spouse_name
        mother_name = father_obj.member_name

    if father_name is not None:
        parent_name += "父" if flag == 1 else '养父'
        parent_name += father_name + "，"
    if mother_name is not None and mother_name != "":
        parent_name += "母" if flag == 1 else '养母'
        parent_name += mother_name.replace(";", "、") + "，"

    return parent_name


# 获取配偶名字信息
def get_spouse_name(member_obj):
    spouse_name = ""
    spouse_label = "妻" if member_obj.sex == 1 else '夫'
    if member_obj.spouse_name is not None:
        if member_obj.spouse_name.strip() != "":
            spouse_name = spouse_label + member_obj.spouse_name.replace(";", "、") + "，"
    return spouse_name


# 获取子女信息
def get_child_info(member_queue, member_obj, member_dict):
    child_info = ""
    son_count = 0
    daughter_count = 0

    child_list = sorted(member_obj.child_list, key=lambda child: child.order_seq)
    child_names = ""
    step_info = ""

    for child_obj in child_list:
        if child_obj.step_father_id is None or child_obj.step_father_id == member_obj.member_id:
            # 插入前驱成员节点
            if child_obj.pre_member_id is not None and child_obj.pre_member_id != 0:
                member_queue.put(member_dict.get(child_obj.pre_member_id))

            # 插入当前成员节点
            member_queue.put(child_obj)

            # 插入后继成员节点
            if child_obj.next_member_id is not None and child_obj.next_member_id != 0:
                member_queue.put(member_dict.get(child_obj.next_member_id))

        # 当子女名字待考时，直接以下划线代替
        cur_child_name = child_obj.member_name if child_obj.member_name != '待考' else '____'
        child_names = child_names + cur_child_name

        # 针对女性子女，添加性别
        if child_obj.sex == 0:
            daughter_count += 1
        else:
            son_count += 1
        child_names += "(女) " if child_obj.sex == 0 else " "


        # 出嗣情况
        if child_obj.step_father_id is not None and child_obj.step_father_id != member_obj.member_id:
            step_father_id = child_obj.step_father_id
            step_father_obj = member_obj = member_dict.get(step_father_id)
            if step_father_obj is None:
                print("step father not exist", step_father_id)
            else:
                step_info = step_info + child_obj.member_name + "出继"+step_father_obj.member_name + "，"

    if child_names != "":
        child_info += "有"
        if son_count != 0:
            child_info += "{0}子".format(get_chinese_number(son_count))
        if daughter_count != 0:
            child_info += "{0}女".format(get_chinese_number(daughter_count))
        child_info += "：" + child_names[:-1].replace(" ", "、")

    if step_info != "":
        child_info += "。其中，" + step_info
    return child_info


# 获取描述信息
def get_description(member_obj):
    description = ""
    if member_obj.description is not None:
        if member_obj.description.strip() != "":
            description = member_obj.description.strip()
    return description


def get_career(member_obj):
    career = ""
    if member_obj.career is not None:
        if member_obj.career.strip() != "":
            career = member_obj.career
    return career


def get_spouse_description(member_obj):
    spouse_description = ""
    if member_obj.spouse_description is not None:
        spouse_description = member_obj.spouse_description.strip()

    if spouse_description != "":
        if spouse_description[-1] != "。":
            spouse_description += "。"
        if member_obj.sex == 0:
            spouse_description = "其夫" + spouse_description
        else:
            spouse_description = "其妻" + spouse_description
    return spouse_description


def get_subtype(member_obj):
    subtype = member_obj.subtype
    if subtype is None or subtype == "":
        return ""
    if subtype.find(';') == -1:
        return subtype+"分支"
    return ""


def gen_book(member_dict, first_member_id, file_name):
    descent_no_tag = 'A'
    member_name_tag = 'B'
    member_description_tag = 'C'

    member_queue = Queue()

    member_obj = member_dict.get(first_member_id)
    if member_obj is None:
        print("line_no=171, member_id:{member_id} not exist".format(member_id=first_member_id))
        return

    file = open(file_name, "w", encoding='UTF-8')
    member_queue.put(member_obj)
    cur_descent_no = member_obj.descent_no
    file.write("## 第 " + str(member_obj.descent_no) + " 世" + descent_no_tag + '\n')

    while not member_queue.empty():
        record_content = ""
        member_obj = member_queue.get()

        # 如果名字为待考，则不出现在世系中
        if member_obj.member_name == '待考':
            continue

        member_obj.print_out()
        if member_obj.descent_no != cur_descent_no:
            record_content += "## 第 " + str(member_obj.descent_no) + " 世" + descent_no_tag + '\n'
            cur_descent_no = member_obj.descent_no

        record_content += "**<font size=4>" + member_obj.member_name + member_name_tag + "\n" + "</font>** <font " \
                                                                                                "size=3> "

        # 当且仅当性别为女性时，需要标注性别
        sex = "" if member_obj.sex == 1 else "女，"
        record_content += sex

        # 分支信息
        subtype = get_subtype(member_obj)
        if subtype != "":
            record_content += subtype + "，"
        # 父母信息
        parent_name = get_parent_name(member_dict, member_obj)
        record_content += parent_name

        # 生父母信息
        if member_obj.step_father_id is not None:
            bio_parent_name = get_parent_name(member_dict, member_obj, 2)
            record_content += bio_parent_name

        # 配偶信息
        spouse_name = get_spouse_name(member_obj)
        record_content += spouse_name

        # 子女信息
        if member_obj.child_list is None:
            continue
        child_info = get_child_info(member_queue, member_obj, member_dict)
        record_content += child_info
        if record_content[-1] == "，":
            record_content = record_content[:-1]
        record_content += "。"

        # 职业
        career = get_career(member_obj)
        if career != "":
            record_content += career + "，"

        # 描述
        description = get_description(member_obj)
        if description != "":
            record_content += description + "。"

        # 其配偶描述
        spouse_description = get_spouse_description(member_obj)
        record_content += spouse_description

        if record_content[-1] == "，":
            record_content = record_content[:-1] + "。"
        record_content += "</font>"
        record_content += member_description_tag

        file.write(record_content + "\n")
    file.close()