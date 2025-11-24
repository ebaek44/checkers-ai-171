from BoardClasses import Move 
from BoardClasses import Board 
import time 
import copy

# Keep a const variable for infinity for iterative dfs and for the alpha-beta pruning 
INF = 10**9 

class StudentAI(): 
    """ 
    - Main bulk of the work for the checkers AI 
    - The main function is get_move() which will find the most optimal move at each turn in a checkers game 
    """ 
    def __init__(self, col, row, p): 
        self.col = col 
        self.row = row 
        self.p = p 
        self.board = Board(col, row, p) 
        self.board.initialize_game() 
        self.color = None  # Will be determined in get_move
        self.opponent = {1: 2, 2: 1} 
        self.threshold = 0.8 


    @staticmethod 
    def flatten_moves(moves_by_piece):
      
        res = [] 
        for bucket in moves_by_piece: 
            res.extend(bucket) 
        return res 

    @staticmethod
    def evaluate(board, color): 
        """ 
        This will look at our count vs the opponents count to see which side is "winning"
        More indepth hueristics by looking at if its a king and giving an edge to better position
        """ 
        score = 0
        
        # Piece values
        PAWN_VALUE = 100
        # Kings are worth 1.5x regular pieces
        KING_VALUE = 150 
     
        for row in range(board.row):
            for col in range(board.col):
                checker = board.board[row][col]
                if checker.color == ".":
                    continue
                
                piece_color = checker.color
                is_king = checker.is_king
                
                # Calculate piece value
                piece_value = KING_VALUE if is_king else PAWN_VALUE
                
                # Add positional bonus when pieces r moved up
                if not is_king:
                    if piece_color == "B": 
                        piece_value += row * 5  
                    else:  
                        piece_value += (board.row - 1 - row) * 5
                
            
                center_distance = abs(col - board.col // 2)
                piece_value += (board.col // 2 - center_distance) * 2
                
        
                if (piece_color == "B" and color == 1) or (piece_color == "W" and color == 2):
                    score += piece_value
                else:
                    score -= piece_value
        
        return score 
    
    def dfs(self, board, d, deadline, alpha, beta, color): 
        """ 
        This is the dfs that will apply moves going up to to a certain depth (d) 
        simulating the alpha/beta scores for both user and opponent or until timed out 
        
        """ 
        # Check time first to look if past deadline 
        if time.perf_counter() >= deadline: 
            return 0, True
        
        moves_by_piece = board.get_all_possible_moves(color) 
        
        # Base case: depth 0 or no legal moves 
        if d == 0 or not moves_by_piece: 
            score = self.evaluate(board, color) 
            return score, False 
        
        moves = self.flatten_moves(moves_by_piece) 
        best_score = -INF 
        
        for mv in moves: 
            # Time check before expanding child 
            if time.perf_counter() >= deadline: 
                return 0, True 
            
            board_copy = copy.deepcopy(board)
            board_copy.make_move(mv, color)
            
            # Negamax: child called with opposite color and negated window 
            opp_color = 3 - color 
            opp_score, timed_out = self.dfs(
                board_copy, 
                d - 1, 
                deadline,
                -beta,  # note the negation and swap 
                -alpha, 
                opp_color 
            )
            
            # Check for timeout 
            if timed_out: 
                return 0, True 
            
            # Our score is negative of opponent's 
            my_score = -opp_score 
            
            if my_score > best_score: 
                best_score = my_score 
            
            if my_score > alpha: 
                alpha = my_score 
            
            # Alpha-beta cutoff 
            if alpha >= beta: 
                break 
        
        return best_score, False 
        
    def get_move(self, move): 
       
        # Determine our color based on first move
        if self.color is None:
            if len(move.seq) == 0:
                # Empty move means we go first
                self.color = 1
            else:
                # We received opponent's move, so we go second
                self.color = 2
        
        if len(move.seq) > 0:
            self.board.make_move(move, self.opponent[self.color])
        
        # Get all possible moves for our color
        moves = self.board.get_all_possible_moves(self.color) 
        if not moves: 
            return Move([]) 
        
        moves = self.flatten_moves(moves) 
        if not moves:
            return Move([])
        
        deadline = self.threshold + time.perf_counter() 
        best_move = moves[0] 
        
        # Iterative deepening
        for d in range(1, INF): 
            # When we are out of time we dont start another loop 
            if time.perf_counter() >= deadline: 
                break 
            
            alpha = -INF 
            beta = INF 
            curr_depth_best_move = None  # Don't initialize to best_move
            curr_depth_best_score = -INF 
            
            for mv in moves: 
                # If we are out of time mid iteration then dont use this depth's best move 
                if time.perf_counter() >= deadline: 
                    curr_depth_best_move = None 
                    break 
                
                # Make a copy of the board and simulate the move
                board_copy = copy.deepcopy(self.board)
                board_copy.make_move(mv, self.color) 
                
                opp_score, timed_out = self.dfs(
                    board_copy, 
                    d - 1, 
                    deadline, 
                    -beta, 
                    -alpha, 
                    self.opponent[self.color]
                )
                
                # If we timed out mid iteration we cannot trust this depth 
                if timed_out: 
                    curr_depth_best_move = None 
                    break 
                
                # So our score is the opposite of the opponents score 
                my_score = -opp_score 
                
                # If the score is better than the current best score then update the optimal move 
                if my_score > curr_depth_best_score: 
                    curr_depth_best_score = my_score 
                    curr_depth_best_move = mv 

                if my_score > alpha: 
                    alpha = my_score 

                if alpha >= beta: 
                    break 

            if curr_depth_best_move is not None: 
                best_move = curr_depth_best_move 
            else: 
                break

        self.board.make_move(best_move, self.color)
        
        return best_move