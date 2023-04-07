from game import Game, Board, Player, INITIAL_STATE
import agent 

def main():
    RANDOM_AGENT_1 = Player(agent.minimax_agent,"minimax_agent ",1)
    RANDOM_AGENT_2 = Player(agent.minimax_position_agent,"minimax_position_agent",-1)
    i = 30
    count = 0
    turn = -1
    while i > 0:
        turn = -turn
        temp = RANDOM_AGENT_1
        RANDOM_AGENT_1 = RANDOM_AGENT_2
        RANDOM_AGENT_2 = temp
        board = Board(INITIAL_STATE)
        
        game = Game(RANDOM_AGENT_1,RANDOM_AGENT_2,board)
        result = game.loop()
        i-=1  
        if result == turn:
            count+=1
    print(count)

if __name__ == "__main__":
    main()