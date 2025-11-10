from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move

from BoardClasses import Move
from BoardClasses import Board
import time
import random

INF = 10**9


def _flatten(buckets):
    """Board.get_all_possible_moves returns List[List[Move]]; flatten to List[Move]."""
    # Loop through buckets, extend result list with each bucket
    # Return flattened list
    pass


class MCTSNode:
    """A node in the MCTS search tree"""
    
    def __init__(self, board, parent=None, move=None, color=None):
        # Store: board, parent, move, color
        # Initialize: children=[], wins=0.0, visits=0, untried_moves=None
        pass
    
    def is_fully_expanded(self):
        """Have we tried all possible moves from this position?"""
        # Return True if untried_moves exists and is empty
        # Otherwise return False
        pass
    
    def is_terminal(self):
        """Is the game over at this node?"""
        # Call self.board.is_win(1)
        # Return True if result != 0 (game over), False otherwise
        pass
    
    def ucb1_score(self, exploration=1.414):
        """Balance trying promising moves vs exploring unknowns"""
        # If visits==0, return infinity (always try unexplored first)
        # Calculate: win_rate + exploration * sqrt(parent.visits / (1 + visits))
        # Return the score
        pass
    
    def best_child(self):
        """Pick child with highest UCB1 score"""
        # Use max() with key=lambda to find child with highest ucb1_score()
        # Return that child
        pass
    
    def add_child(self, move, board, color):
        """Create and add a new child node"""
        # Create new MCTSNode with board, parent=self, move, color
        # Append to self.children
        # Return the child
        pass


class StudentAI:
    
    def __init__(self, col, row, p):
        # Store: col, row, p
        # Create board: Board(col, row, p), call initialize_game()
        # Set: color=None, opponent={1:2, 2:1}, time_per_move=0.80
        pass

    def get_move(self, move: Move):
        """Called by game engine each turn"""
        # If move exists: determine color if needed, apply opponent's move
        # Else: set self.color = 1
        # Get legal moves, flatten them
        # If no moves: return Move([])
        # If 1 move: apply it and return it
        # Otherwise: call run_mcts(), apply best move, return it
        pass
    
    def run_mcts(self, legal_moves):
        """Run MCTS iterations until time runs out"""
        # Create root node with copy.deepcopy(self.board)
        # Set deadline = time.perf_counter() + self.time_per_move
        # While time remains: select -> expand -> simulate -> backpropagate
        # Return move from child with most visits
        pass
    
    def select(self, node):
        """Walk down tree picking best children using UCB1"""
        # While not terminal and fully expanded: node = node.best_child()
        # Return the node
        pass
    
    def expand(self, node):
        """Add one new child node by trying an unexplored move"""
        # If terminal: return node
        # If untried_moves is None: get all legal moves, store them, store next_color
        # If no untried moves: return node
        # Pop random move, create new board with move applied
        # Add child, return child
        pass
    
    def simulate(self, node):
        """Play random moves until game ends"""
        # Copy board, determine starting color
        # Loop max 100 times: check is_win, get moves, pick random, apply it
        # Return 1.0 if we won, 0.0 if lost, 0.5 if tie
        pass
    
    def backpropagate(self, node, result):
        """Update win/visit statistics from node back to root"""
        # While node exists: increment visits, add result (flip for opponent)
        # Move to parent: node = node.parent
        pass
    
    def evaluate_position(self, board):
        """Quick heuristic based on piece count"""
        # Get my_pieces and opp_pieces from board.black_count/white_count
        # Return my_pieces / (my_pieces + opp_pieces)
        pass




#check this added below, greedy minimax
from BoardClasses import Move, Board
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
        
        # Get all legal moves
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
        
        # Apply and return best move
        self.board.make_move(best_move, self.color)
        return best_move
    
    def evaluate(self, board):
        """Simple evaluation: piece count difference"""
        if self.color == 1:  # Black
            my_pieces = board.black_count
            opp_pieces = board.white_count
        else:  # White
            my_pieces = board.white_count
            opp_pieces = board.black_count
        
        return my_pieces - opp_pieces