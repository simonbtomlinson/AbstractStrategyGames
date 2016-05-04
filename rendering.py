import graphviz

from abstract_game import AbstractGame

node_styles = {
    'double_edge': {'peripheries': '2'},
    'thick_edges': {'style': 'bold'},
    'box': {'shape': 'box'}
}


def render(game: AbstractGame, graph_name):
    dg = graphviz.Digraph(graph_name, engine="neato")
    dg.attr("graph", {"splines": 'true', "overlap": "scale"})
    dg.attr("edge", {"minlen": "1"})
    drawn_labels = set()
    for node, data in game.game_graph.nodes_iter(data=True):
        if node == game.initial_gamestate:
            dg.node(node, **node_styles['box'])
        elif game.is_losing_position(node, game.player1):
            dg.node(node, **node_styles['double_edge'])
        elif game.is_losing_position(node, game.player2):
            dg.node(node, **node_styles['thick_edges'])
    for from_node, to_node, edge_data in game.game_graph.edges_iter(keys=True):
        if (to_node, from_node, edge_data) in drawn_labels:
            label = ''
        else:
            label = edge_data
        dg.edge(from_node, to_node, label=label)
        drawn_labels.add((from_node, to_node, edge_data))
    return dg


def render_to_png(game, graph_name):
    dg = render(game, graph_name)
    export_to_png(dg)
    dg.view()


def export_to_png(graph):
    with open(graph.name + '.png', 'wb') as outfile:
        outfile.write(graph.pipe('png'))


def render_pong_hau_ki_board():
    g = graphviz.Graph("PongHauKiBoard", engine="neato")
    visible_edges = (
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 4),
        (3, 5),
        (4, 5),
    )
    invisible_edges = ((1, 5),)
    for v1, v2 in visible_edges:
        g.edge(str(v1), str(v2))
    for v1, v2 in invisible_edges:
        g.edge(str(v1), str(v2), style='invis')
    g.pipe()
    g.view()


def render_berry_patch_scramble_board():
    g = graphviz.Graph("BerryPatchScrambleBoard", engine="neato")
    visible_edges = (
        (1, 2),
        (2, 3),
        (3, 5),
        (5, 6),
        (6, 7),
        (1, 4),
        (2, 4),
        (3, 4),
        (5, 4),
        (6, 4),
        (7, 4)
    )
    invisible_edges = (
        (1, 7),
    )
    for v1, v2 in visible_edges:
        g.edge(str(v1), str(v2))
    for v1, v2 in invisible_edges:
        g.edge(str(v1), str(v2), style='invis')
    with open(g.name + '.png', 'wb') as outfile:
        outfile.write(g.pipe('png'))
    g.view()


def render_mu_torere_board():
    mu_torere_edge_swaps = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 0),
        (8, 0),
        (8, 1),
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 7)
    )
    g = graphviz.Graph("MuTorereBoard", engine="neato")
    for v1, v2 in mu_torere_edge_swaps:
        g.edge(str(v1 + 1), str(v2 + 1))
    export_to_png(g)
    g.view()

if __name__ == '__main__':
    # render_pong_hau_ki_board()
    # render_berry_patch_scramble_board()
    render_mu_torere_board()