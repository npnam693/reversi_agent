from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from game import Game, Board, Player, INITIAL_STATE
import agent

BOARD_SIZE = 64
ENCODED_SIZE = 32

board_input = Input(shape=(BOARD_SIZE + 1,))

dense1 = Dense(ENCODED_SIZE, activation='relu')(board_input)
dense2 = Dense(ENCODED_SIZE, activation='relu')(dense1)

output = Dense(2, activation='sigmoid')(dense2)

# The autoencoder is the full model that feeds back to itself
model = Model(board_input, output)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

amount_games = 2000
epochs = 200
batch_size = 32
X, y = [], []

RANDOM_AGENT_1 = Player(agent.random_agent,"random_agent 1",1)
RANDOM_AGENT_2 = Player(agent.best_now_agent,"random_agent 2",-1)
while amount_games > 0:
    temp = RANDOM_AGENT_1
    RANDOM_AGENT_1 = RANDOM_AGENT_2
    RANDOM_AGENT_2 = temp
    board = Board(INITIAL_STATE)

    game = Game(RANDOM_AGENT_1, RANDOM_AGENT_2, board)
    result = game.loop()
    amount_games -= 1
    if(result == 0):
        continue
    for step in board.store:
        flatten_step = [cell for row in step[0] for cell in row]
        X.append(flatten_step + [step[1]])
        y.append([0, 1] if step[1] == result else [1, 0])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, train_size=0.8)
callback = EarlyStopping(monitor='loss', patience=3)
model.fit(X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                shuffle=True,
                validation_data=(X_test, y_test),
                callbacks=[callback])

print(model.evaluate(X_train, y_train))

model.save('reversi_neural.h5')







