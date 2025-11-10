from BoardClasses import Move, Board
from random import randint
import copy

def all_choices(buckets):
    out = []
    for bucket in buckets:
        out.extend(bucket)
    return out

class StudentAI:
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = None
        self.opponent = {1: 2, 2: 1}

    def get_move(self, move: Move):

        if move and getattr(move, "seq", None):
            if self.color is None:
                self.color = 2
            self.board.make_move(move, self.opponent[self.color])
        else:
            if self.color is None:
                self.color = 1

        legal = all_choices(self.board.get_all_possible_moves(self.color))
        if not legal:
            return Move([])
        best_move = legal[0]
        best_score = -999999
        
        for m in legal:
            test_board = copy.deepcopy(self.board)
            test_board.make_move(m, self.color)

            score = self.evaluate(test_board)
            
            if score > best_score:
                best_score = score
                best_move = m

        self.board.make_move(best_move, self.color)
        return best_move
    
    def evaluate(self, board):

        if self.color == 1:
            my_pieces = board.black_count
            opp_pieces = board.white_count
        else:
            my_pieces = board.white_count
            opp_pieces = board.black_count
        
        return my_pieces - opp_pieces