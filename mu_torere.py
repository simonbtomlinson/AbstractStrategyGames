from rendering import render_to_png

from pong_hau_ki import PongHauKiGame, EMPTY_SPACE, PLAYER_1, PLAYER_2

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


def cycle(li: list):
    li.insert(0, li.pop())


class MuTorereGame(PongHauKiGame):

    def canonicalize(self, gamestate):
        center = gamestate[-1]
        edges_list = [c for c in gamestate[:-1]]
        possible_canonical_forms = []
        for e_list in (edges_list, edges_list[::-1]):
            for i in range(len(e_list)):
                possible_canonical_forms.append(''.join(e_list))
                cycle(e_list)
        return min(possible_canonical_forms) + center

    def possible_moves(self, gamestate: str, player):
        # Edge swaps don't have the mu torere rule.
        for swap in mu_torere_edge_swaps:
            if {gamestate[i] for i in swap} == {player, EMPTY_SPACE}:  # Use a set so that order doesn't matter.
                # This is a legal move.
                # Swap involves the center, Mu Torere rules apply
                if len(gamestate) - 1 in swap:
                    edge_index, center_index = sorted(swap)
                    edge = gamestate[:-1]
                    if self.other_player(player) not in (edge[edge_index - 1], edge[(edge_index + 1) % len(edge)]):
                        continue
                gs_list = list(gamestate)
                gs_list[swap[0]], gs_list[swap[1]] = gs_list[swap[1]], gs_list[swap[0]]  # Swap the characters
                yield ''.join(gs_list)

if __name__ == '__main__':
    initial_position = ''.join([PLAYER_1] * 4 + [PLAYER_2] * 4 + [EMPTY_SPACE])
    different_position = ''.join([PLAYER_1, PLAYER_2] * 4 + [EMPTY_SPACE])
    game = MuTorereGame(PLAYER_1, PLAYER_2, different_position)
    game.play(lookahead=3)
    render_to_png(game, 'mu_torere')