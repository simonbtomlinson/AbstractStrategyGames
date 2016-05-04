from negamax_lookahead_version.rendering import render_to_png

from abstract_game import AbstractGame

PLAYER_1 = 'A'
PLAYER_2 = 'B'
EMPTY_SPACE = '0'

pong_hau_ki_swaps = (
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 3),
    (2, 4),
    (3, 4)
)


class PongHauKiGame(AbstractGame):
    def possible_moves(self, gamestate, player):
        for swap in pong_hau_ki_swaps:
            if {gamestate[i] for i in swap} == {player, EMPTY_SPACE}:  # Use a set so that order doesn't matter.
                # This is a legal move.
                gs_list = list(gamestate)
                gs_list[swap[0]], gs_list[swap[1]] = gs_list[swap[1]], gs_list[swap[0]]  # Swap the characters
                yield ''.join(gs_list)

    def is_losing_position(self, gamestate, player):
        return len(list(self.possible_moves(gamestate, player))) == 0

    def is_winning_position(self, gamestate, player):
        return self.is_losing_position(gamestate, self.other_player(player))

    def canonicalize(self, gamestate):
        return min(gamestate, gamestate[::-1])


if __name__ == '__main__':

    initial_position = ''.join([PLAYER_1, PLAYER_2, EMPTY_SPACE, PLAYER_2, PLAYER_1])
    game = PongHauKiGame(PLAYER_1, PLAYER_2, initial_position)

    game.play(lookahead=2)
    render_to_png(game, 'phk')
