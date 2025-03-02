from math import trunc
from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import random
import copy


class Node:
    def __init__(self, move=None, parent=None, turn = None):
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.turn = turn
        self.terminal = False

    def is_leaf(self):
        return self.children == []

    def best_child(self, exploration_weight=1.4):
        return max(self.children,
                   key=lambda child: child.value / (child.visits + 1e-6) + exploration_weight * math.sqrt(
                       math.log(self.visits + 1) / (child.visits + 1e-6)))

    def add_Children(self, board):
        nextTurn = 0
        if self.turn == 2:
            nextTurn = 1
        else:
            nextTurn = 2
        moves = board.get_all_possible_moves(self.turn)
        if moves == []:
            self.terminal = True
            return
        for _ in moves:
            for j in _:
                self.children.append(Node(j, self, nextTurn))


def monte_carlo_tree_search(root, board):
    for _ in range(500):
        b = copy.deepcopy(board)
        leaf = traverse(root,b)
        simulation_result = rollout(leaf, b, root.turn)
        backpropagate(leaf, simulation_result)

    return root.best_child().move


# function for node traversal
def traverse(node, board):
    n = node
    while not n.is_leaf():
        n = n.best_child()
        board.make_move(n.move, n.parent.turn)

    n.add_Children(board)
    if n.terminal or n.children == []:
        return n
    if n.visits == 0:
        return n
    n = n.best_child()
    board.make_move(n.move, n.turn)
    return n



# function for the result of the simulation
def rollout(node, board, team):
    turn = node.turn
    while True:
        moves = board.get_all_possible_moves(turn)
        if moves == []:
            if turn == 1:
                turn = 2
            else:
                turn = 1
            v = board.is_win(turn)
            if v ==0:
                return .5
            if v == team:
                return 1
            else:
                return 0
        move = random.choice(random.choice(moves))
        board.make_move(move, turn)
        if turn == 1:
            turn = 2
        else:
            turn = 1

# function for backpropagation
def backpropagate(node, result):
    node.value += result
    node.visits += 1
    if node.parent == None:
        return
    backpropagate(node.parent, result)


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
        self.turns = 0
        
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        m = None
        if self.turns < 0:
            m = random.choice(random.choice(self.board.get_all_possible_moves(self.color)))
        else:
            n = Node(None, None, self.color)
            n.add_Children(self.board)
            m = monte_carlo_tree_search(n, copy.deepcopy(self.board))
        #m = random.choice(random.choice(self.board.get_all_possible_moves(self.color)))
        self.board.make_move(m, self.color)
        self.turns += 1
        return m


if __name__ == '__main__':
    b = Board(8,8,2)
    b.initialize_game()
    b.show_board()
    t = 1
    while True:
        print(t)
        m = None
        if t == 2:
            n = Node(None, None, t)
            n.add_Children(b)
            m = monte_carlo_tree_search(n, b)
        else:
            m = b.get_all_possible_moves(t)
            m = random.choice(random.choice(m))
        b.make_move(m, t)
        b.show_board()

        if t ==2:
            t = 1
        else:
            t = 2
        if b.is_win(t):
            print('penis', t)
            exit(0)