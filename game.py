import pygame as pg
import numpy as np
import time
BG_COLOR = (86, 102, 245) 
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BOARD_SIZE = 8
DELAY_TIME = 0
TOTAL_TIME = 60
LIMIT_TIME = 20
INITIAL_STATE = [[0,0,0,0,0,0,0,0], 
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,1,-1,0,0,0],
                 [0,0,0,-1,1,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0]]
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 500
class Board:
    def __init__(self, board_state):
        self.board_state = board_state
        
    def draw_board(self, surface):
        surface.fill(BG_COLOR)
        for i in range(1, BOARD_SIZE):
            x = i * 60
            pg.draw.line(surface, BLACK_COLOR, (x, 0), (x, 480), 2)
            pg.draw.line(surface, BLACK_COLOR, (0, x), (480, x), 2)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board_state[row][col] == 1:
                    pg.draw.circle(surface, WHITE_COLOR, (col * 60 + 30, row * 60 + 30), 25)
                elif self.board_state[row][col] == -1:
                    pg.draw.circle(surface, BLACK_COLOR, (col * 60 + 30, row * 60 + 30), 25)
    
    def update_board(self, position, player):
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
        
        def make_move(board, row, col, turn):
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
        valid_move = get_valid_moves(self.board_state,player)
        if valid_move == []: valid_move.append(None)
        if position not in valid_move: return False
        if position == None: return True
        (x,y) = position
        self.board_state = make_move(self.board_state,x,y,player)
        return True
    def get_board(self):
        return self.board_state
class Player:
    def __init__(self,agent,name,turn) -> None:
        self.agent = agent
        self.name = name
        self.turn = turn
        self.time = TOTAL_TIME
        self.last_move = None
    def move(self,board_state):
        start_time = time.perf_counter()
        ans = self.agent(board_state,self.turn,self.time)
        elapsed_time = time.perf_counter() - start_time
        if elapsed_time > LIMIT_TIME:
            return -1
        self.time -= elapsed_time
        if elapsed_time < 0:
            return -1
        self.last_move = ans
        return ans
class Game:
    def __init__(self,player1,player2,board):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player1 = player1
        self.player2 = player2
        self.board = board
    def end_check(self):
        cur_board = self.board.get_board()
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
        
        return get_valid_moves(cur_board,1)==[] and get_valid_moves(cur_board,-1)==[]
    
    def win_check(self):
        cur_board = self.board.get_board()
        player1= 0
        player2 = 0
        for i in cur_board:
            for j in i:
                if j==1: player1+=1
                elif j==-1: player2+=1
        if player1>player2: return 1
        if player2>player1: return -1
        return 0
    
    def draw_turn(self,player1,player2,playerturn):
        font = pg.font.Font(None, 30)
        player1_name = font.render(player1.name, True, BLACK_COLOR)
        player2_name = font.render(player2.name, True, BLACK_COLOR)
        player1_last_move = font.render("Last Move: "+str(player1.last_move), True, BLACK_COLOR)
        player2_last_move = font.render("Last Move: "+str(player2.last_move), True, BLACK_COLOR)
        player1_time = font.render(f"Time left: {player1.time:.5f}s", True, BLACK_COLOR)
        player2_time = font.render(f"Time left: {player2.time:.5f}s", True, BLACK_COLOR)
        player1_name_rect = player1_name.get_rect()
        player2_name_rect = player2_name.get_rect()
        player1_last_move_rect = player1_last_move.get_rect()
        player2_last_move_rect = player2_last_move.get_rect()
        player1_time_rect = player1_time.get_rect()
        player2_time_rect = player2_time.get_rect()
        player1_name_rect.center = (WINDOW_WIDTH - 200, 50)
        player2_name_rect.center = (WINDOW_WIDTH - 200, WINDOW_HEIGHT/2)
        player1_last_move_rect.center = (WINDOW_WIDTH - 100, 100)
        player2_last_move_rect.center = (WINDOW_WIDTH - 100, WINDOW_HEIGHT/2+50)
        player1_time_rect.center = (WINDOW_WIDTH - 100, 150)
        player2_time_rect.center = (WINDOW_WIDTH - 100, WINDOW_HEIGHT/2+100)
        if playerturn == 1:
            player1_name = font.render(player1.name+"'s Turn", True, RED_COLOR)
        else:
            player2_name = font.render(player2.name+"'s Turn", True, RED_COLOR)
        self.screen.blit(player1_name, player1_name_rect)
        self.screen.blit(player2_name, player2_name_rect)
        self.screen.blit(player1_last_move, player1_last_move_rect)
        self.screen.blit(player2_last_move, player2_last_move_rect)
        self.screen.blit(player1_time, player1_time_rect)
        self.screen.blit(player2_time, player2_time_rect)
    
    def loop(self):
        turn = self.player1.turn
        self.board.draw_board(self.screen)
        self.draw_turn(self.player1,self.player2,turn)
        pg.display.flip()
        looping = False
        winner = 0
        move = None
        while not looping:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    looping = False
            if turn == self.player1.turn:
                move=self.player1.move(self.board.board_state)
                if move == -1:
                    winner = -1
                    pg.display.flip()
                    break
            else: 
                move=self.player2.move(self.board.board_state)
                if move == -1:
                    winner = 1
                    pg.display.flip()
                    break
            valid_move = self.board.update_board(move,turn)
            if not valid_move:
                if turn==1:
                    winner = -1
                    pg.display.flip()
                    # time.sleep(DELAY_TIME)
                    break
                else:
                    winner = 1
                    pg.display.flip()
                    # time.sleep(DELAY_TIME) 
                    break
            self.board.draw_board(self.screen)
            self.draw_turn(self.player1,self.player2,turn)
            pg.display.flip()

            looping = self.end_check()
            if looping:
                winner = self.win_check()
            else:
                turn = - turn
        
        
        
        
        time.sleep(5)
        if winner == self.player1.turn: 
            title = self.player1.name + " win"
        elif winner == self.player2.turn: 
            title = self.player2.name + " win"
        else: 
            title = self.player1.name + " draw " + self.player2.name
        print(winner, title)
        return winner
