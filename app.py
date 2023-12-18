from flask import Flask, request, render_template, redirect, session
from boggle import Boggle

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

# init boggle game and board
boggle_game = Boggle()
board = boggle_game.make_board()
print(board)


@app.route('/')
def index():
    """Show boggle board and word guess form."""

    # Store board in the session
    session['board'] = board

    return render_template("board.html", board=board)

@app.route('/check-word')
def check_word():
    """Check if word is valid"""

    # guess guess from query string
    word_guess = request.args["word-guess"]

    # check guess: "ok", "not-on-board", "not-word"
    result = boggle_game.check_valid_word(board, word_guess)

    return render_template("board.html", board=board)

