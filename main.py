from game import Game, Board, Player, INITIAL_STATE
import agent 


def main():
    RANDOM_AGENT_1 = Player(agent.random_agent,"random",1)
    RANDOM_AGENT_2 = Player(agent.best_now_agent,"AI",-1)
    board = Board(INITIAL_STATE)
    player1 = RANDOM_AGENT_1
    player2 = RANDOM_AGENT_2
    ### chọn AGENT MÀ MÌNH MUỐN
    i = 30
    count = 0
    while i > 0:
        board = Board(INITIAL_STATE)
        game = Game(player1,player2,board)
        result = game.loop()
        i-=1  
        if result == -1:
            count+=1
    print(count)

if __name__ == "__main__":
    main()