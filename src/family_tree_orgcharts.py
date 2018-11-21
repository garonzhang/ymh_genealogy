import json
from member import MemberNode


def get_pre_part():
    pre_part = """
            <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <title>Organization Chart Plugin</title>
          <link rel="icon" href="img/logo.png">
          <link rel="stylesheet" href="css/font-awesome.min.css">
          <link rel="stylesheet" href="css/jquery.orgchart.min.css">
          <link rel="stylesheet" href="css/style.css">
          <style type="text/css">
            .orgchart { background: #87CEEB; }
            .orgchart td.left, .orgchart td.right, .orgchart td.top { border-color: #aaa; }
            .orgchart td>.down { background-color: #aaa; }
            .orgchart .middle-level .title { background-color: #458B74; }
            .orgchart .middle-level .content { border-color: #006699; }
            .orgchart .product-dept .title { background-color: #009933; }
            .orgchart .product-dept .content { border-color: #009933; }
            .orgchart .rd-dept .title { background-color: #993366; }
            .orgchart .rd-dept .content { border-color: #993366; }
            .orgchart .pipeline1 .title { background-color: #996633; }
            .orgchart .pipeline1 .content { border-color: #996633; }
            .orgchart .frontend1 .title { background-color: #cc0066; }
            .orgchart .frontend1 .content { border-color: #cc0066; }
          </style>
        </head>
        <body>
          <div id="chart-container"></div>
        
          <script type="text/javascript" src="js/jquery.min.js"></script>
          <script type="text/javascript" src="js/jquery.orgchart.min.js"></script>
          <script type="text/javascript">
            $(function() {
        
            var datasource = 
                 """
    return pre_part


def draw_node(member_dict, cur_node):
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
        draw_node(member_dict, child_node)


def get_data_part(member_dict, first_member_id):
    member_obj = member_dict.get(first_member_id)

    member_name = member_obj.member_name
    sex = member_obj.sex
    spouse_name = member_obj.spouse_name
    descent_no = member_obj.descent_no

    first_node = MemberNode(first_member_id, member_name, sex, spouse_name, descent_no, "middle-level")
    draw_node(member_dict, first_node)
    result = json.dumps(first_node, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)+";"
    print(result)
    return result


def get_post_part():
    post_part = """
                var nodeTemplate = function(data) {
                  return `
                    <div class="title">${data.member_name}</div>
                    <div class="content">${data.spouse_name}</div>
                    <div class="content">${data.descent_no}</div>
                  `;
                };
            
                var oc = $('#chart-container').orgchart({
                  'data' : datasource,
                  'nodeTemplate': nodeTemplate
                });
            
              });
              </script>
              </body>
            </html>
                """
    return post_part


def draw_tree(member_dict, first_member_id, file_name):
    pre_part = get_pre_part()
    data_part = get_data_part(member_dict, first_member_id)
    post_part = get_post_part()

    html_content = pre_part + data_part + post_part
    file = open(file_name, "w", encoding='UTF-8')
    file.write(html_content)
    file.close()
