from BoardClasses 
import Move from BoardClasses 
import Board import time 
import copy
#The following part should be completed by students. 
#Students can modify anything except the class name and exisiting functions and varibles. 
# Keep a const variable for infinity for iterative dfs and for the alpha-beta pruning 
INF = 10**9 
class StudentAI(): 
    """ 
    - Main bulk of the work for the checkers AI 
    - The main function is get_move() which will find the most optimal move at each turn in a checkers game 
    """ 
    def __init__(self,col,row,p): 
        self.col = col 
        self.row = row 
        self.p = p 
        self.board = Board(col,row,p) 
        self.board.initialize_game() 
        self.color = '' 
        self.opponent = {1:2,2:1} 
        self.color = 2 
        self.threshold = 0.8 
        # 0.8 seconds at each depth till cutoff 
        @staticmethod 
        def flatten_moves(moves_by_piece):
             """ 
             Board.get_all_possible_moves returns List[List[Move]]; flatten to List[Move]. 
             """ 
             res = [] 
             for bucket in moves_by_piece: 
                res.extend(bucket) 
                return res 
        
        @staticmethod
        def evaluate(board, color): 
            """ 
            This will look at our count vs the opponents count to see which side is "winning" 
            """ 
            if color == 1: 
                my_pieces = board.black_count 
                opp_pieces = board.white_count 
            else: 
                my_pieces = board.white_count 
                opp_pieces = board.black_count 
            
            return my_pieces - opp_pieces 
        

        def dfs(self, board, d, deadline, al, be, color): # (board, depth, deadline, alpha, beta, color) 
            """ 
            This is the dfs that will apply moves going up to to a certain depth (d) 
            simulating the alpha/beta scores for both user and opponent or until timed out 
            @parameters: simulating moves on board, using alpha (al) and beta(be) scores to move flipping each move with color 
            @returns: tuple of score which is the opponents score, and timed_out which will tell if deadliune was hit during search 
            """ 
            # Check time first to look if past deadline 
            if time.perf_counter() >= deadline: 
                return 0, True
            
            moves_by_piece = board.get_all_possible_moves(color) 
            
            # Base case: depth 0 or no legal moves 
            if d == 0 or not moves_by_piece: 
                score = self.evaluate(board, color) 
                # score is garbage when timed out 
                return score, False 
            
            moves = self.flatten_moves(moves_by_piece) 
            best_score = -INF 
            alpha = al 
            beta = be 
            
            for mv in moves: 
                # Time check before expanding child 
                if time.perf_counter() >= deadline: 
                    return 0, True 
                mv_copy = copy.deepcopy(mv)
                board.make_move(mv_copy, color) 
                # Negamax: child called with opposite color and negated window 
                opp_color = 3 - color 
                opp_score, timed_out = self.dfs(
                    board, 
                    d - 1, 
                    deadline,
                    -beta, # note the negation and swap 
                    -alpha, 
                    opp_color 
                    ) 
                    
                # back track that decision 
                board.undo() 
                
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
            
            
            def get_move(self,move): 
                """ 
                Main function for the StudentAI Uses alpha-beta pruning with iterative dfs to find the most optimal move 
                @parameters: move is the last move that has been done by the opponent 
                @return: Will either return the best move from all possible moves or in certain edge cases return None 
                """ 
                # If the opponent has made a previous move apply it to the board 
                if len(move) != 0: 
                    self.board.make_move(move,self.opponent[self.color]) 
                else: 
                    self.color = 1 
                
                moves = self.board.get_all_possible_moves(self.color) 
                if not moves: 
                    return Move([]) 
                
                moves = self.flatten_moves(moves) 
                deadline = self.threshold + time.perf_counter() 
                # This will be our return variable, give it a move to start 
                best_move = moves[0] 
                
                for d in range(1, INF): 
                    # When we are out of time we dont start another loop 
                    if time.perf_counter() >= deadline: 
                        break 
                    
                    alpha = -INF 
                    beta = INF 
                    curr_depth_best_move = best_move 
                    curr_depth_best_score = -INF 
                    
                    for mv in moves: 
                        # If we are out of time mid iteration then dont use this depth's best move 
                        if time.perf_counter() >= deadline: 
                            curr_depth_best_move = None 
                            break 
                        
                        # now simulate a move and then pop the move (using a copy)
                        mv_copy = copy.deepcopy(mv)
                        self.board.make_move(mv_copy, self.color) 
                        # The dfs will return the opponent's score and if it was timed out during the iteration 
                        # Also give everything flipped as it is our opponents "move" 
                        opp_score, timed_out = self.dfs(self.board, d - 1, deadline, -beta, -alpha, self.opponent[self.color]) 

                        self.board.undo()
                        
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
                        
                        # Update alpha with score if it is a better score 
                        if my_score > alpha: 
                            alpha = my_score 
                        # If alpha >= beta then break loop (alpha-beta pruning) 
                        if alpha >= beta: 
                            break 
                            
                        # Only update best move if the loop finished before threshold 
                        if curr_depth_best_move is not None: 
                            best_move = curr_depth_best_move 
                        else: 
                            break 
                        
                        return best_move 
                        
