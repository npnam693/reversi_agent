def is_valid_move(board, row, col, turn):
    if board[row][col] != 0:
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            
            r = row + i
            c = col + j
            found_opponent = False
            
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if board[r][c] == 0:
                    break
                if board[r][c] == turn:
                    if found_opponent:
                        return True
                    break
                found_opponent = True
                r += i
                c += j
    return False

def get_valid_moves(board, turn):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, turn):
                valid_moves.append((row, col))
    return valid_moves
    
def make_move(board, move, turn):
    row, col = move
    new_board = [row[:] for row in board]
    
    new_board[row][col] = turn
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            
            r = row + i
            c = col + j
            flipped = False
            to_flip = []
            
            while r >= 0 and r < 8 and c >= 0 and c < 8:
                if new_board[r][c] == 0:
                    break
                if new_board[r][c] == turn:
                    flipped = True
                    break
                to_flip.append((r, c))
                r += i
                c += j
            
            if flipped:
                for (r, c) in to_flip:
                    new_board[r][c] = turn
    return new_board

def get_score(cur_state, player_to_move):
    score = 0
    for row in cur_state:
        for col in row:
            if col == player_to_move:
                score += 1
            elif col == 0:
                score += 0
            else:
                score -= 1
    return score


POSITION_SCORES = [[25, 0, 6, 5, 5, 6, 0, 25],
                    [ 0, 0, 1, 1, 1, 1, 0,  0],
                    [ 6, 1, 4, 3, 3, 4, 1,  6],
                    [ 5, 1, 3, 2, 2, 3, 1,  5],
                    [ 5, 1, 3, 2, 2, 3, 1,  5],
                    [ 6, 1, 4, 3, 3, 4, 1,  6],
                    [ 0, 0, 1, 1, 1, 1, 0,  0],
                    [25, 0, 6, 5, 5, 6, 0, 25]]

POSITION_SCORES2 = [[95,10,80,75,75,80,10,95],
                    [10,10,45,45,45,45,10,10],
                    [65,40,70,50,50,70,40,65],
                    [60,40,40,40,40,40,40,60],
                    [60,40,40,40,40,40,40,60],
                    [65,40,70,50,50,70,40,65],
                    [10,10,45,45,45,45,10,10],
                    [95,10,65,60,60,65,10,95]]
def get_score_position_stragety(cur_state, player_to_move):
    score = 0
    for row in range (0,8):
        for col in range (0,8):
            if (cur_state[row][col] == player_to_move):
                score += POSITION_SCORES2[row][col]
    return score