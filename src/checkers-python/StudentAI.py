from random import randint
from BoardClasses import Move
from BoardClasses import Board

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
        
        # Try to find a capturing move first
        best_move = None
        max_captures = 0
        
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                current_move = moves[i][j]
                # If move sequence length > 2, it's a capturing move
                if len(current_move.seq) > 2:
                    captures = (len(current_move.seq) - 2) // 2
                    if captures > max_captures:
                        max_captures = captures
                        best_move = (i, j)
        
        # If we found a capturing move, use it
        if best_move is not None:
            index, inner_index = best_move
        else:
            # Otherwise, choose randomly like before
            index = randint(0,len(moves)-1)
            inner_index = randint(0,len(moves[index])-1)
        
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move