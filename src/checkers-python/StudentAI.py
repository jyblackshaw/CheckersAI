from random import randint
from BoardClasses import Move, Board

class StudentAI:
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
    
    def evaluate_move(self, move, is_endgame=False):
        """Score a move based on simple criteria"""
        score = 0
        end_pos = move.seq[-1]  # Final position
        
        # Capture moves
        if len(move.seq) > 2:
            score += 100 * ((len(move.seq) - 2) // 2)  # 100 points per capture
            
        # King moves
        if (self.color == 1 and end_pos[0] == self.row - 1) or \
           (self.color == 2 and end_pos[0] == 0):
            score += 50  # 50 points for becoming king
            
        # Edge moves are safer
        if end_pos[1] == 0 or end_pos[1] == self.col - 1:
            score += 10  # 10 points for edge position
            
        # In endgame, prefer advancing
        if is_endgame:
            if self.color == 1:  # Moving down
                score += end_pos[0] * 5
            else:  # Moving up
                score += (self.row - end_pos[0]) * 5
                
        return score
    
    def is_endgame(self):
        """Simple check if we're in endgame - count pieces"""
        piece_count = 0
        for row in range(self.row):
            for col in range(self.col):
                if self.board.board[row][col] != 0:
                    piece_count += 1
        return piece_count <= 10  # Endgame if 10 or fewer pieces
    
    def find_best_move(self, moves):
        """Find best move using simple scoring"""
        best_score = float('-inf')
        best_move = (0, 0)  # Default to first move
        endgame = self.is_endgame()
        
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                current_move = moves[i][j]
                score = self.evaluate_move(current_move, endgame)
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
        
        return best_move
    
    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        
        moves = self.board.get_all_possible_moves(self.color)
        index, inner_index = self.find_best_move(moves)
        move = moves[index][inner_index]
        
        self.board.make_move(move, self.color)
        return move