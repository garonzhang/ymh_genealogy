import networkx as nx
import matplotlib.pyplot as plt

def draw_org():
    G = nx.DiGraph()
    G.add_node("ROOT")
    for i in range(5):
        G.add_node("Child_%i" % i)
        G.add_node("child_%i" % i)
        G.add_node("child_%i" % i)

        G.add_edge("ROOT", "Child_%i" % i)
        G.add_edge("Child_%i" % i, "child_%i" % i)
        G.add_edge("child_%i" % i, "child_%i" % i)

    plt.title('The OrgChart Demo')
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=True, arrows=False, node_shape='s', node_size=2000,  alpha=0.5, font_size=10)
    plt.savefig('../output/nx_org.svg')


def draw_circular():
    try:
        import pygraphviz
        from networkx.drawing.nx_agraph import graphviz_layout
    except ImportError:
        try:
            import pydot
            from networkx.drawing.nx_pydot import graphviz_layout
        except ImportError:
            raise ImportError("This example needs Graphviz and either "
                              "PyGraphviz or pydot")

    G = nx.balanced_tree(3, 5)
    pos = graphviz_layout(G, prog='twopi', args='')
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
    plt.axis('equal')
    plt.savefig('../output/nx_circular.svg')


if __name__ == "__main__":
    draw_org()
    #draw_circular()