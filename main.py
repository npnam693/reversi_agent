from game import Game, Board, Player, INITIAL_STATE
import agent 
import mcts_agent
from _1915939_2013827_2014914_2010951 import select_move

def main():
    RANDOM_AGENT_1 = Player(agent.random_agent,"random_agent",1)
    RANDOM_AGENT_2 = Player(agent.neural_network,"My agent",-1)
    # RANDOM_AGENT_2 = Player(agent.best_now_agent,"best now",-1)
    i = 30
    count = 0
    myturn = -1
    while i > 0:
        temp = RANDOM_AGENT_1
        RANDOM_AGENT_1 = RANDOM_AGENT_2
        RANDOM_AGENT_2 = temp
        board = Board(INITIAL_STATE)
        
        game = Game(RANDOM_AGENT_1,RANDOM_AGENT_2,board)
        result = game.loop()
        i-=1  
        if result == -1:
            count+=1
        myturn = -myturn
    print(count)

if __name__ == "__main__":
    main()



    