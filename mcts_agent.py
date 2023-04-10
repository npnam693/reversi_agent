from utils import get_valid_moves, make_move, end_check, win_check
import math, random

class Node:
    def __init__(self, board, parent, myTurn, turn, move = None):
        self.board = board
        self.myTurn = myTurn
        self.parent = parent
        self.childs = None
        self.wins = 0
        self.games = 0

        self.expansion = False
        self.isVisited = False
        self.turn = turn
        self.move = move

    def select_child(self):
        if not self.expansion:
            self.expansion = True
            moves = get_valid_moves(self.board, self.turn)
            self.childs = [Node(make_move(self.board, move, self.turn), self, self.myTurn, -self.turn, move) for move in moves]
        
        if len(self.childs) == 0:
            self.propagate(False)
            return None

        for child in self.childs:
            if not child.isVisited:
                child.isVisited = True
                return child
        
        ln_games = math.log(self.games)

        def uct_score(child):
            return (child.wins / child.games) + 1.41 * math.sqrt(ln_games / child.games)
        good_child = max(self.childs, key=uct_score)
       
        return good_child.select_child()
    
    def simulate(self):
        cur_board = self.board.copy()

        now_turn = self.turn
        
        while end_check(cur_board):
            cur_board = make_move(cur_board, random.choice(get_valid_moves(cur_board, now_turn)))
            now_turn = -now_turn

        if win_check(cur_board) == self.myTurn:
            return True
        else: return False

    def propagate(self, isWin):
        self.games += 1
        self.wins = self.wins + 1 if isWin else self.wins
        if self.parent is not None:
            self.parent.propagate(isWin)


def MTCS_Agent(cur_state, player_to_move, remain_time):
    root_node = Node(cur_state, None, player_to_move, player_to_move)
    iterator = 1000

    while iterator >= 0:
        iterator -=1
        node = root_node.select_child()
        if node is None: return None
        if end_check(node.board) and win_check(node.board) == player_to_move:
            break
        resultSimulate = node.simulate()
        node.propagate(resultSimulate)
    



    ln_games = math.log(root_node.games)
    
    def uct_score(child):
            return (child.wins / child.games) + 1.41 * math.sqrt(ln_games / child.games)
    good_child = max(root_node.childs, key=uct_score)
    return good_child.move
        