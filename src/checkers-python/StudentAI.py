
from BoardClasses import Move, Board
from random import randint
import copy

def _flatten(buckets):
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
        # Apply opponent's move
        if move and getattr(move, "seq", None):
            if self.color is None:
                self.color = 2
            self.board.make_move(move, self.opponent[self.color])
        else:
            if self.color is None:
                self.color = 1
        
        #list of all legal moves
        legal = _flatten(self.board.get_all_possible_moves(self.color))
        if not legal:
            return Move([])
        
        # Evaluate each move and pick best
        best_move = legal[0]
        best_score = -999999
        
        for m in legal:
            # Try the move
            test_board = copy.deepcopy(self.board)
            test_board.make_move(m, self.color)
            
            # Evaluate position
            score = self.evaluate(test_board)
            
            if score > best_score:
                best_score = score
                best_move = m
        
        # applies the best move and returns the best move
        self.board.make_move(best_move, self.color)
        return best_move
    
    def evaluate(self, board):

        if self.color == 1:  # Black
            my_pieces = board.black_count
            opp_pieces = board.white_count
        else:  # White
            my_pieces = board.white_count
            opp_pieces = board.black_count
        
        return my_pieces - opp_pieces