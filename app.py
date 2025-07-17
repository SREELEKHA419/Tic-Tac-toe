from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def check_winner(board, player):
    win_states = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(all(board[i] == player for i in line) for line in win_states)

def get_ai_move(board, ai_symbol, player_symbol):
    for i in range(9):
        if board[i] == "":
            board[i] = ai_symbol
            if check_winner(board, ai_symbol):
                return i
            board[i] = ""

    for i in range(9):
        if board[i] == "":
            board[i] = player_symbol
            if check_winner(board, player_symbol):
                board[i] = ""
                return i
            board[i] = ""

    if board[4] == "":
        return 4
    for i in [0, 2, 6, 8]:
        if board[i] == "":
            return i
    for i in [1, 3, 5, 7]:
        if board[i] == "":
            return i
    return -1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    player = data['player']
    ai = "O" if player == "X" else "X"

    if not check_winner(board, player) and any(cell == "" for cell in board):
        ai_move = get_ai_move(board, ai, player)
        if ai_move != -1:
            board[ai_move] = ai

    winner = None
    if check_winner(board, ai):
        winner = ai
    elif check_winner(board, player):
        winner = player
    elif all(cell != "" for cell in board):
        winner = "Draw"

    return jsonify({
        "board": board,
        "winner": winner
    })

if __name__ == '__main__':
    app.run(debug=True)
