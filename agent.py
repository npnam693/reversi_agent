from utils import is_valid_move, get_valid_moves, make_move, get_score, get_score_position_stragety, heuristic
import random



def random_agent(cur_state, player_to_move, remain_time):
    valid_moves = get_valid_moves(cur_state,player_to_move)
    if valid_moves == []: return None
    else: return random.choice(valid_moves)

def best_now_agent(cur_state, player_to_move, remain_time):
    moves = get_valid_moves(cur_state, player_to_move)
    best_score = -1000
    best_move = False
    for move in moves:
        newboard = cur_state.copy()
        newboard = make_move(newboard, move, player_to_move)
        score = get_score(newboard, player_to_move)
        if score > best_score:
            best_move = move
            best_score = score
    if not best_move : return None
    return best_move

def minimax_agent(cur_state, player_to_move, remain_time):
    def minimax(cur_state, depth, player_to_move):
        moves = get_valid_moves(cur_state, player_to_move)
        if (len(moves) == 0): return None
        best_move = moves[0]
        best_score = -1000
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, player_to_move)
            score = min_play(newboard, depth-1, player_to_move)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(cur_state, depth, player_to_move):
        if depth == 0:
            return get_score(cur_state, player_to_move)
        moves = get_valid_moves(cur_state, -player_to_move)
        best_score = 1000
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, -player_to_move)
            score = max_play(newboard, depth-1, player_to_move)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(cur_state, depth, player_to_move):
        if depth == 0:
            return get_score(cur_state, player_to_move)
        moves = get_valid_moves(cur_state, player_to_move)
        best_score = -1000
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, player_to_move)
            score = min_play(newboard, depth-1, player_to_move)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score    
    return minimax(cur_state, 3, player_to_move)

def minimax_position_agent(cur_state, player_to_move, remain_time):
    def minimax(cur_state, depth, player_to_move):
        moves = get_valid_moves(cur_state, player_to_move)
        if (len(moves) == 0): return None
        best_move = moves[0]
        best_score = -1000
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, player_to_move)
            score = min_play(newboard, depth-1, player_to_move)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(cur_state, depth, player_to_move):
        if depth == 0:
            return get_score_position_stragety(cur_state, player_to_move)
        moves = get_valid_moves(cur_state, -player_to_move)
        best_score = 1000
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, -player_to_move)
            score = max_play(newboard, depth-1, player_to_move)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(cur_state, depth, player_to_move):
        if depth == 0:
            return get_score_position_stragety(cur_state, player_to_move)
        moves = get_valid_moves(cur_state, player_to_move)
        best_score = -1000
        for move in moves:
            newboard = cur_state.copy()
            newboard = make_move(newboard, move, player_to_move)
            score = min_play(newboard, depth-1, player_to_move)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score    
    return minimax(cur_state, 2, player_to_move)