from load_members import load_members
import family_tree_orgcharts
import genealogy_book
import circular_tree


def gen_circular_tree():
    first_member_id = 1
    circular_tree.gen_graph(member_dict, first_member_id)


def gen_book():
    first_member_id = 1
    file_name = "../output/family_book.md"
    genealogy_book.gen_book(member_dict, first_member_id, file_name)


def gen_tree():
    first_member_id = 151
    if first_member_id == 1:
        file_name = "../data/orgchart_tree.html"
    else:
        file_name = "../data/orgchart_tmp.html"
    family_tree_orgcharts.draw_tree(member_dict, first_member_id, file_name)


if __name__ == "__main__":
    member_dict = load_members()

    #gen_tree()
    #gen_book()
    gen_circular_tree()

    
