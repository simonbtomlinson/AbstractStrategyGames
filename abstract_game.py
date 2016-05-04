from networkx import MultiDiGraph


class AbstractGame:
    def __init__(self, player1, player2, initial_gamestate):
        self.game_graph = MultiDiGraph()
        self.player1 = player1
        self.player2 = player2
        self.initial_gamestate = self.canonicalize(initial_gamestate)

    def canonicalize(self, gamestate):
        raise NotImplementedError

    def possible_moves(self, gamestate, player):
        raise NotImplementedError

    def other_player(self, player):
        if player == self.player1:
            return self.player2
        elif player == self.player2:
            return self.player1
        else:
            raise ValueError("%s is neither %s nor %s" % (player, self.player1, self.player2))

    def is_winning_position(self, gamestate, player):
        raise NotImplementedError

    def is_losing_position(self, gamestate, player):
        raise NotImplementedError

    def good_moves(self, gamestate, player, lookahead_depth):

        if lookahead_depth == 0:
            yield from self.possible_moves(gamestate, player)
        else:
            lookahead_depth -= 1
            sign = {self.player1: 1, self.player2: -1}

            def is_game_over(gamestate):
                return evaluate_gamestate(gamestate, 0) != 0

            def evaluate_gamestate(gamestate, depth):
                """
                Returns 1 if this gamestate favors the first player, -1 if it favors the second player,
                and 0 if it is neutral.
                """
                if self.is_winning_position(gamestate, self.player1):
                    return 1000 - depth
                elif self.is_winning_position(gamestate, self.player2):
                    return -1000 + depth
                else:
                    return 0

            def negamax(gamestate, current_depth, current_player):
                if is_game_over(gamestate) or current_depth > lookahead_depth:
                    return sign[current_player] * evaluate_gamestate(gamestate, current_depth)
                max_score = -1000
                for possible_gamestate in self.possible_moves(gamestate, current_player):
                    max_score = max(max_score,
                                    -negamax(possible_gamestate, current_depth + 1, self.other_player(current_player)))
                return max_score

            moves_and_lookaheads = {move: -negamax(move, 1, self.other_player(player)) for move in self.possible_moves(gamestate, player)}

            if len(moves_and_lookaheads) == 0:
                return
            best_lookahead = max(moves_and_lookaheads.values())
            good_moves = {self.canonicalize(move) for move, lookahead in moves_and_lookaheads.items() if lookahead == best_lookahead}
            for move in good_moves:
                yield move

    def play(self, lookahead=0):
        new_moves = set()  # A set of node, player tuples containing all new moves that can be played in this graph.

        def play_new_moves():
            new_new_moves = set()  # The moves that will be new after current new moves have been played.
            for gamestate, player in new_moves:
                next_player = self.other_player(player)
                for move_result in self.good_moves(gamestate, player, lookahead):
                    move_result = self.canonicalize(move_result)
                    if move_result not in self.game_graph:  # Add the result to the graph if it's not there.
                        self.game_graph.add_node(move_result, players=set())
                    self.game_graph.add_edge(gamestate, move_result, key=player)  # Add this move to the graph
                    if next_player not in self.game_graph.node[move_result]['players']:
                        self.game_graph.node[move_result]['players'].add(next_player)
                        new_new_moves.add((move_result, next_player))
            new_moves.clear()
            new_moves.update(new_new_moves)

        new_moves.add((self.initial_gamestate, self.player1))
        self.game_graph.add_node(self.initial_gamestate, players=set())

        while len(new_moves) != 0:
            play_new_moves()
        self.game_graph
