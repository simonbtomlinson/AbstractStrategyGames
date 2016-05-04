from negamax_lookahead_version.rendering import render_to_png

from pong_hau_ki import PongHauKiGame, EMPTY_SPACE, PLAYER_1, PLAYER_2

berry_patch_scramble_swaps = (
    (0, 1),
    (1, 2),
    (2, 4),
    (4, 5),
    (5, 6),
    (0, 3),
    (1, 3),
    (2, 3),
    (4, 3),
    (5, 3),
    (6, 3)
)

class BerryPatchScrambleGame(PongHauKiGame):

    def possible_moves(self, gamestate, player):
        for swap in berry_patch_scramble_swaps:
            if {gamestate[i] for i in swap} == {player, EMPTY_SPACE}:  # Use a set so that order doesn't matter.
                # This is a legal move.
                gs_list = list(gamestate)
                gs_list[swap[0]], gs_list[swap[1]] = gs_list[swap[1]], gs_list[swap[0]]  # Swap the characters
                yield ''.join(gs_list)


if __name__ == '__main__':
    initial_position = ''.join([PLAYER_1, PLAYER_2, PLAYER_1, EMPTY_SPACE, PLAYER_2, PLAYER_1, PLAYER_2])
    game = BerryPatchScrambleGame(PLAYER_1, PLAYER_2, initial_position)

    game.play(lookahead=4)
    print(len(game.game_graph))
    render_to_png(game, 'bps')
